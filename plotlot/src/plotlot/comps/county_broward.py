from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Final

import anyio
import httpx
from pydantic import BaseModel, ConfigDict, ValidationError

from plotlot.comps.arcgis import (
    ArcGISFeature,
    ArcGISField,
    ArcGISQuery,
    ArcGISResponseError,
    feature_coordinates,
    get_arcgis_before_deadline,
    parse_arcgis_day,
    parse_arcgis_price,
    query_arcgis_features,
)
from plotlot.comps.models import CompPolicy, CompSubject, Qualification, SaleEvidence
from plotlot.comps.sources import SourceResult

BROWARD_SERVICE_URL: Final = (
    "https://gisweb-adapters.bcpa.net/arcgis/rest/services/BCPA_EXTERNAL_JAN26/MapServer"
)
_YEAR_LAYER_PATTERN: Final = re.compile(r"^(?P<year>\d{4}) Sales$")
_QUALIFICATION_BY_FLAG: Final[dict[str, Qualification]] = {
    "Q": "qualified",
    "U": "disqualified",
}
_FIELD_TAILS: Final = (
    "OBJECTID",
    "FOLIO",
    "FOLIO_NUMBER",
    "SALE_DATE",
    "SALE_AMOUNT",
    "SALE_VER",
    "SALE_YEAR",
)


class BrowardLayerMetadata(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    id: int
    name: str


class BrowardServiceMetadata(BaseModel):
    model_config = ConfigDict(frozen=True, extra="ignore")

    layers: tuple[BrowardLayerMetadata, ...]


@dataclass(frozen=True, slots=True)
class BrowardYearLayer:
    year: int
    layer_id: int


def _policy_years(policy: CompPolicy) -> tuple[int, ...]:
    as_of = date.fromisoformat(policy.as_of)
    month_index = as_of.year * 12 + as_of.month - 1 - policy.months
    first_year = month_index // 12
    return tuple(range(first_year, as_of.year + 1))


def _year_layers(
    metadata: BrowardServiceMetadata,
    required_years: tuple[int, ...],
) -> tuple[BrowardYearLayer, ...]:
    discovered: list[BrowardYearLayer] = []
    for layer in metadata.layers:
        match = _YEAR_LAYER_PATTERN.fullmatch(layer.name)
        if match is None:
            continue
        year = int(match.group("year"))
        if year in required_years:
            discovered.append(BrowardYearLayer(year=year, layer_id=layer.id))
    return tuple(sorted(discovered, key=lambda layer: layer.year, reverse=True))


def _field_by_tail(fields: tuple[ArcGISField, ...], tail: str) -> str:
    matches = tuple(field.name for field in fields if field.name.rsplit(".", 1)[-1] == tail)
    return matches[0] if len(matches) == 1 else ""


def _text(value: str | int | float | bool | None) -> str:
    return "" if value is None else str(value).strip()


def _qualification(value: str) -> Qualification:
    return _QUALIFICATION_BY_FLAG.get(value.upper(), "unknown")


def _map_broward_feature(
    feature: ArcGISFeature,
    fields: tuple[ArcGISField, ...],
    layer: BrowardYearLayer,
    retrieved_at: str,
    source_url: str,
) -> SaleEvidence | None:
    names = {
        tail: _field_by_tail(fields, tail)
        for tail in (
            "OBJECTID",
            "FOLIO",
            "FOLIO_NUMBER",
            "SALE_DATE",
            "SALE_AMOUNT",
            "SALE_VER",
            "SALE_YEAR",
        )
    }
    required = ("FOLIO", "FOLIO_NUMBER", "SALE_DATE", "SALE_AMOUNT", "SALE_VER")
    if any(not names[name] for name in required):
        return None
    attributes = feature.attributes
    parcel_folio = _text(attributes.get(names["FOLIO"]))
    sale_folio = _text(attributes.get(names["FOLIO_NUMBER"]))
    parcel_id = sale_folio or parcel_folio
    sale_year = _text(attributes.get(names["SALE_YEAR"])) if names["SALE_YEAR"] else ""
    conflicts: list[str] = []
    if parcel_folio and sale_folio and parcel_folio != sale_folio:
        conflicts.append("parcel_sale_folio_mismatch")
    if sale_year and sale_year != str(layer.year):
        conflicts.append("sale_year_layer_mismatch")
    coordinates = feature_coordinates(feature)
    qualification_code = _text(attributes.get(names["SALE_VER"]))
    object_id = _text(attributes.get(names["OBJECTID"])) if names["OBJECTID"] else ""
    sale_date = parse_arcgis_day(attributes.get(names["SALE_DATE"]))
    return SaleEvidence(
        evidence_id=f"broward:{layer.year}:{object_id or parcel_id}",
        parcel_id=parcel_id,
        state="FL",
        county="Broward",
        sale_price=parse_arcgis_price(attributes.get(names["SALE_AMOUNT"])),
        sale_date=sale_date,
        date_precision="day" if sale_date else "unknown",
        latitude=coordinates[0] if coordinates is not None else None,
        longitude=coordinates[1] if coordinates is not None else None,
        classification_basis=(
            f"Broward SALE_VER={qualification_code}; property condition at sale unavailable"
        ),
        transaction_status="closed",
        qualification=_qualification(qualification_code),
        qualification_code=qualification_code,
        source_kind="county",
        source_url=source_url,
        source_record_id=object_id,
        retrieved_at=retrieved_at,
        conflict_flags=tuple(conflicts),
    )


async def fetch_broward_candidates(
    subject: CompSubject,
    policy: CompPolicy,
    *,
    client: httpx.AsyncClient | None = None,
    retrieved_at: str | None = None,
) -> SourceResult:
    """Discover exact year sales layers inside the pinned BCPA service."""
    if subject.latitude is None or subject.longitude is None:
        return SourceResult((), "unavailable", ("Subject coordinates are required.",), ())
    owns_client = client is None
    active_client = client or httpx.AsyncClient(
        timeout=httpx.Timeout(connect=5, read=20, write=10, pool=5),
        limits=httpx.Limits(max_connections=20, max_keepalive_connections=10),
        transport=httpx.AsyncHTTPTransport(retries=2),
        follow_redirects=False,
    )
    required_years = _policy_years(policy)
    notes: list[str] = []
    candidates: list[SaleEvidence] = []
    source_urls: list[str] = []
    partial = False
    deadline = anyio.current_time() + 25
    try:
        response = await get_arcgis_before_deadline(
            active_client, BROWARD_SERVICE_URL, params={"f": "json"}, deadline=deadline
        )
        response.raise_for_status()
        metadata = BrowardServiceMetadata.model_validate_json(response.content)
        layers = _year_layers(metadata, required_years)
        found_years = {layer.year for layer in layers}
        missing_years = tuple(year for year in required_years if year not in found_years)
        if missing_years:
            partial = True
            notes.append(f"Broward year layers unavailable: {missing_years}.")
        for layer in layers:
            source_url = f"{BROWARD_SERVICE_URL}/{layer.layer_id}"
            source_urls.append(source_url)
            result = await query_arcgis_features(
                active_client,
                ArcGISQuery(
                    layer_url=source_url,
                    latitude=subject.latitude,
                    longitude=subject.longitude,
                    radius_miles=policy.radius_miles,
                    out_fields=(),
                    out_field_tails=_FIELD_TAILS,
                    max_records=1000,
                ),
                deadline=deadline,
            )
            partial = partial or result.partial
            notes.extend(result.notes)
            timestamp = retrieved_at or datetime.now(timezone.utc).isoformat()
            mapped_count = 0
            malformed_records = 0
            for feature in result.features:
                try:
                    candidate = _map_broward_feature(
                        feature,
                        result.fields,
                        layer,
                        timestamp,
                        source_url,
                    )
                except ValidationError:
                    malformed_records += 1
                    continue
                if candidate is not None:
                    candidates.append(candidate)
                    mapped_count += 1
            if result.features and not mapped_count:
                partial = True
                notes.append(f"Broward {layer.year} metadata lacks required sale fields.")
            if malformed_records:
                partial = True
                notes.append(
                    f"Skipped {malformed_records} malformed Broward {layer.year} sale records."
                )
    except (TimeoutError, ArcGISResponseError, ValidationError, httpx.HTTPError) as error:
        return SourceResult(
            tuple(candidates),
            "partial" if candidates else "unavailable",
            (*notes, f"Broward county source unavailable: {type(error).__name__}: {error}"),
            tuple(source_urls) or (BROWARD_SERVICE_URL,),
        )
    finally:
        if owns_client:
            with anyio.move_on_after(1, shield=True):
                await active_client.aclose()
    return SourceResult(
        tuple(candidates),
        "partial" if partial else "available",
        tuple(notes),
        tuple(source_urls),
    )
