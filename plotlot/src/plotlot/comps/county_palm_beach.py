from __future__ import annotations

from datetime import datetime, timezone
from typing import Final

import anyio
import httpx
from pydantic import ValidationError

from plotlot.comps.arcgis import (
    ArcGISFeature,
    ArcGISField,
    ArcGISQuery,
    ArcGISResponseError,
    feature_coordinates,
    parse_arcgis_day,
    parse_arcgis_price,
    query_arcgis_features,
)
from plotlot.comps.models import CompPolicy, CompSubject, Qualification, SaleEvidence
from plotlot.comps.sources import SourceResult

PALM_BEACH_SALES_URL: Final = (
    "https://gis.pbcgov.org/arcgis/rest/services/Parcels/PARCEL_INFO/FeatureServer/4"
)
_FIELDS: Final = (
    "OBJECTID",
    "PARID",
    "PARCEL_NUMBER",
    "CONDO",
    "SITE_ADDR_STR",
    "SALEKEY",
    "SALE_DATE",
    "BOOK",
    "PAGE",
    "PRICE",
    "INSTRUMENT",
    "QUAL_CODE",
    "Q_SALE_DATE",
)
_QUALIFIED_CODES: Final = frozenset({"Q", "QC", "QD", "QL", "QM", "QO", "QP"})


def _text(value: str | int | float | bool | None) -> str:
    return "" if value is None else str(value).strip()


def _qualification(code: str) -> Qualification:
    return "qualified" if code.upper() in _QUALIFIED_CODES else "disqualified"


def _recorded_document(instrument: str, book: str, page: str) -> str:
    reference = f"OR {book}/{page}" if book and page else ""
    return " ".join(part for part in (instrument, reference) if part)


def _canonical_names(fields: tuple[ArcGISField, ...]) -> frozenset[str]:
    return frozenset(field.name for field in fields)


def _map_feature(feature: ArcGISFeature, retrieved_at: str) -> SaleEvidence:
    attributes = feature.attributes
    parid = _text(attributes.get("PARID"))
    parcel_number = _text(attributes.get("PARCEL_NUMBER"))
    condo = _text(attributes.get("CONDO")).upper()
    condo_map_hierarchy = (
        condo == "YES"
        and len(parid) == 10
        and parid.isdecimal()
        and len(parcel_number) == 17
        and parcel_number.isdecimal()
        and parcel_number.startswith(parid)
    )
    parcel_id = parcel_number if condo_map_hierarchy else parid or parcel_number
    conflicts = (
        ("parcel_identifier_mismatch",)
        if parid and parcel_number and parid != parcel_number and not condo_map_hierarchy
        else ()
    )
    qualification_code = _text(attributes.get("QUAL_CODE"))
    sale_date = parse_arcgis_day(attributes.get("SALE_DATE"))
    coordinates = feature_coordinates(feature)
    book = _text(attributes.get("BOOK"))
    page = _text(attributes.get("PAGE"))
    instrument = _text(attributes.get("INSTRUMENT"))
    source_record_id = _text(attributes.get("SALEKEY"))
    return SaleEvidence(
        evidence_id=f"palm-beach:{source_record_id or parcel_id}",
        parcel_id=parcel_id,
        state="FL",
        county="Palm Beach",
        address=_text(attributes.get("SITE_ADDR_STR")),
        sale_price=parse_arcgis_price(attributes.get("PRICE")),
        sale_date=sale_date,
        date_precision="day" if sale_date else "unknown",
        latitude=coordinates[0] if coordinates is not None else None,
        longitude=coordinates[1] if coordinates is not None else None,
        classification_basis=(
            f"Palm Beach QUAL_CODE={qualification_code}; property condition at sale unavailable"
        ),
        transaction_status="closed",
        qualification=_qualification(qualification_code),
        qualification_code=qualification_code,
        source_kind="county",
        source_url=PALM_BEACH_SALES_URL,
        source_record_id=source_record_id,
        recorded_document=_recorded_document(instrument, book, page),
        retrieved_at=retrieved_at,
        review_notes=f"County PARID={parid}; PARCEL_NUMBER={parcel_number}; CONDO={condo}.",
        conflict_flags=conflicts,
    )


async def fetch_palm_beach_candidates(
    subject: CompSubject,
    policy: CompPolicy,
    *,
    client: httpx.AsyncClient | None = None,
    retrieved_at: str | None = None,
) -> SourceResult:
    """Fetch Palm Beach's one transaction slot without substituting Q_SALE_DATE."""
    if subject.latitude is None or subject.longitude is None:
        return SourceResult((), "unavailable", ("Subject coordinates are required.",), ())
    owns_client = client is None
    active_client = client or httpx.AsyncClient(
        timeout=httpx.Timeout(connect=5, read=20, write=10, pool=5),
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        transport=httpx.AsyncHTTPTransport(retries=2),
        follow_redirects=False,
    )
    try:
        result = await query_arcgis_features(
            active_client,
            ArcGISQuery(
                layer_url=PALM_BEACH_SALES_URL,
                latitude=subject.latitude,
                longitude=subject.longitude,
                radius_miles=policy.radius_miles,
                out_fields=_FIELDS,
            ),
        )
    except (TimeoutError, ArcGISResponseError, ValidationError, httpx.HTTPError) as error:
        return SourceResult(
            (),
            "unavailable",
            (f"Palm Beach county source unavailable: {type(error).__name__}: {error}",),
            (PALM_BEACH_SALES_URL,),
        )
    finally:
        if owns_client:
            with anyio.move_on_after(1, shield=True):
                await active_client.aclose()
    required_fields = frozenset({"PARID", "SALEKEY", "SALE_DATE", "PRICE", "QUAL_CODE"})
    missing_fields = required_fields - _canonical_names(result.fields)
    if missing_fields:
        return SourceResult(
            (),
            "unavailable",
            (f"Palm Beach metadata lacks required fields: {tuple(sorted(missing_fields))}.",),
            (PALM_BEACH_SALES_URL,),
        )
    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    candidates: list[SaleEvidence] = []
    malformed_records = 0
    for feature in result.features:
        try:
            candidates.append(_map_feature(feature, timestamp))
        except ValidationError:
            malformed_records += 1
    notes = list(result.notes)
    notes.append(
        "Current parcel acreage and property use are not used because at-sale values are unavailable."
    )
    if malformed_records:
        notes.append(f"Skipped {malformed_records} malformed Palm Beach sale records.")
    return SourceResult(
        tuple(candidates),
        "partial" if result.partial or malformed_records else "available",
        tuple(notes),
        (PALM_BEACH_SALES_URL,),
    )
