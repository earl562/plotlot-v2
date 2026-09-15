from __future__ import annotations

from datetime import date, datetime, timezone
from typing import Final, assert_never

import anyio
import httpx
from pydantic import ValidationError

from plotlot.comps.arcgis import (
    ArcGISFeature,
    ArcGISQuery,
    ArcGISResponseError,
    feature_coordinates,
    parse_arcgis_day,
    parse_arcgis_price,
    query_arcgis_features,
)
from plotlot.comps.models import (
    CompCategory,
    CompPolicy,
    CompSubject,
    PropertyType,
    Qualification,
    SaleEvidence,
)
from plotlot.comps.dates import DateWindow
from plotlot.comps.sources import SourceResult

MIAMI_DADE_SALES_URL: Final = (
    "https://gisweb.miamidade.gov/arcgis/rest/services/MD_ComparableSales/MapServer/5"
)
_FIELDS: Final = (
    "FOLIO",
    "TRUE_SITE_ADDR",
    "DOS_1",
    "OR_BK_1",
    "OR_PG_1",
    "PRICE_1",
    "QU_FLG_1",
    "VI_1",
    "DOS_2",
    "OR_BK_2",
    "OR_PG_2",
    "PRICE_2",
    "QU_FLG_2",
    "VI_2",
    "DOS_3",
    "OR_BK_3",
    "OR_PG_3",
    "PRICE_3",
    "QU_FLG_3",
    "VI_3",
)
_QUALIFICATION_BY_FLAG: Final[dict[str, Qualification]] = {
    "Q": "qualified",
    "U": "disqualified",
}


def _text(value: str | int | float | bool | None) -> str:
    return "" if value is None else str(value).strip()


def _recorded_document(book: str, page: str) -> str:
    return f"OR {book}/{page}" if book and page else ""


def _classification(flag: str, slot: int) -> tuple[PropertyType, CompCategory, str]:
    normalized = flag.upper()
    if normalized == "V":
        return "land", "land", f"Miami-Dade VI_{slot}=V at-sale flag"
    if normalized == "I":
        return "unknown", "unknown", f"Miami-Dade VI_{slot}=I at-sale flag"
    return "unknown", "unknown", "Miami-Dade at-sale condition unavailable"


def _qualification(flag: str) -> Qualification:
    return _QUALIFICATION_BY_FLAG.get(flag.upper(), "unknown")


def _map_feature(feature: ArcGISFeature, retrieved_at: str) -> tuple[SaleEvidence, ...]:
    attributes = feature.attributes
    folio = _text(attributes.get("FOLIO"))
    address = _text(attributes.get("TRUE_SITE_ADDR"))
    coordinates = feature_coordinates(feature)
    latitude = coordinates[0] if coordinates is not None else None
    longitude = coordinates[1] if coordinates is not None else None
    candidates: list[SaleEvidence] = []
    for slot in (1, 2, 3):
        raw_date = attributes.get(f"DOS_{slot}")
        raw_price = attributes.get(f"PRICE_{slot}")
        book = _text(attributes.get(f"OR_BK_{slot}"))
        page = _text(attributes.get(f"OR_PG_{slot}"))
        qualification_code = _text(attributes.get(f"QU_FLG_{slot}"))
        vacant_improved = _text(attributes.get(f"VI_{slot}"))
        if all(
            value in (None, "")
            for value in (raw_date, raw_price, book, page, qualification_code, vacant_improved)
        ):
            continue
        property_type, category, classification_basis = _classification(vacant_improved, slot)
        sale_date = parse_arcgis_day(raw_date)
        candidates.append(
            SaleEvidence(
                evidence_id=f"miami-dade:{folio}:slot-{slot}",
                parcel_id=folio,
                state="FL",
                county="Miami-Dade",
                address=address,
                sale_price=parse_arcgis_price(raw_price),
                sale_date=sale_date,
                date_precision="day" if sale_date else "unknown",
                latitude=latitude,
                longitude=longitude,
                property_type=property_type,
                category=category,
                classification_basis=classification_basis,
                transaction_status="closed",
                qualification=_qualification(qualification_code),
                qualification_code=qualification_code,
                source_kind="county",
                source_url=MIAMI_DADE_SALES_URL,
                recorded_document=_recorded_document(book, page),
                retrieved_at=retrieved_at,
            )
        )
    return tuple(candidates)


async def fetch_miami_dade_candidates(
    subject: CompSubject,
    policy: CompPolicy,
    *,
    client: httpx.AsyncClient | None = None,
    retrieved_at: str | None = None,
) -> SourceResult:
    """Fetch Miami-Dade parcel sales without mixing the three transaction slots."""
    if subject.latitude is None or subject.longitude is None:
        return SourceResult((), "unavailable", ("Subject coordinates are required.",), ())
    window = DateWindow(date.fromisoformat(policy.as_of), policy.months)
    match subject.category:
        case "land":
            land_only = True
        case "resale" | "new_construction" | "incomplete" | "unknown":
            land_only = False
        case unreachable:
            assert_never(unreachable)
    where = " OR ".join(
        f"(DOS_{slot} >= '{window.cutoff:%Y%m%d}' AND DOS_{slot} <= '{window.as_of:%Y%m%d}'"
        + (f" AND VI_{slot} = 'V'" if land_only else "")
        + ")"
        for slot in (1, 2, 3)
    )
    query = ArcGISQuery(
        layer_url=MIAMI_DADE_SALES_URL,
        latitude=subject.latitude,
        longitude=subject.longitude,
        radius_miles=policy.radius_miles,
        out_fields=_FIELDS,
        where=where,
        max_records=1000,
    )
    owns_client = client is None
    active_client = client or httpx.AsyncClient(
        timeout=httpx.Timeout(connect=5, read=20, write=10, pool=5),
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        transport=httpx.AsyncHTTPTransport(retries=2),
        follow_redirects=False,
    )
    try:
        result = await query_arcgis_features(active_client, query)
    except (TimeoutError, ArcGISResponseError, ValidationError, httpx.HTTPError) as error:
        return SourceResult(
            (),
            "unavailable",
            (f"Miami-Dade county source unavailable: {type(error).__name__}: {error}",),
            (MIAMI_DADE_SALES_URL,),
        )
    finally:
        if owns_client:
            with anyio.move_on_after(1, shield=True):
                await active_client.aclose()
    field_names = frozenset(field.name for field in result.fields)
    required_fields = frozenset(
        {"FOLIO"}
        | {f"{prefix}_{slot}" for prefix in ("DOS", "PRICE", "QU_FLG", "VI") for slot in (1, 2, 3)}
    )
    missing_fields = required_fields - field_names
    if missing_fields:
        return SourceResult(
            (),
            "unavailable",
            (f"Miami-Dade metadata lacks required fields: {tuple(sorted(missing_fields))}.",),
            (MIAMI_DADE_SALES_URL,),
        )
    timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
    candidates: list[SaleEvidence] = []
    malformed_records = 0
    for feature in result.features:
        try:
            candidates.extend(_map_feature(feature, timestamp))
        except ValidationError:
            malformed_records += 1
    notes = list(result.notes)
    notes.append(
        f"Parcel search requires a sale slot within {window.cutoff} through {window.as_of}"
        + (" with its own vacant-sale flag." if land_only else ".")
    )
    notes.append("Current LOT_SIZE is not used because at-sale lot size is unavailable.")
    if malformed_records:
        notes.append(f"Skipped {malformed_records} malformed Miami-Dade parcel records.")
    status = "partial" if result.partial or malformed_records else "available"
    return SourceResult(tuple(candidates), status, tuple(notes), (MIAMI_DADE_SALES_URL,))
