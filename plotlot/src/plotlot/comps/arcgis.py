from __future__ import annotations

from datetime import datetime, timezone
from typing import Final, assert_never
from urllib.parse import urlsplit

import anyio
import httpx
from pydantic import ValidationError
from shapely.geometry import Polygon

from plotlot.comps.arcgis_models import (
    JsonScalar as JsonScalar,
    UnsupportedArcGISHostError as UnsupportedArcGISHostError,
    ArcGISResponseError as ArcGISResponseError,
    ArcGISErrorPayload as ArcGISErrorPayload,
    ArcGISErrorEnvelope as ArcGISErrorEnvelope,
    ArcGISField as ArcGISField,
    ArcGISAdvancedCapabilities as ArcGISAdvancedCapabilities,
    ArcGISMetadata as ArcGISMetadata,
    ArcGISGeometry as ArcGISGeometry,
    ArcGISFeature as ArcGISFeature,
    ArcGISFeatureEnvelope as ArcGISFeatureEnvelope,
    ArcGISQuery as ArcGISQuery,
    ArcGISFeatureResult as ArcGISFeatureResult,
)

_ALLOWED_HOSTS: Final = frozenset(
    {
        "gis.pbcgov.org",
        "gisweb-adapters.bcpa.net",
        "gisweb.miamidade.gov",
    }
)


def parse_arcgis_day(value: JsonScalar) -> str:
    match value:
        case bool() | None:
            return ""
        case int() | float():
            numeric_day = str(int(value))
            if len(numeric_day) == 8:
                try:
                    return datetime.strptime(numeric_day, "%Y%m%d").date().isoformat()
                except ValueError:
                    return ""
            try:
                return datetime.fromtimestamp(value / 1000, tz=timezone.utc).date().isoformat()
            except (OSError, OverflowError, ValueError):
                return ""
        case str():
            cleaned = value.strip()
            if len(cleaned) == 8 and cleaned.isdigit():
                try:
                    return datetime.strptime(cleaned, "%Y%m%d").date().isoformat()
                except ValueError:
                    return ""
            try:
                return datetime.fromisoformat(cleaned[:10]).date().isoformat()
            except ValueError:
                return ""
        case unreachable:
            assert_never(unreachable)


def parse_arcgis_price(value: JsonScalar) -> float | None:
    if isinstance(value, bool) or value is None:
        return None
    cleaned = str(value).strip().replace("$", "").replace(",", "")
    try:
        return float(cleaned)
    except ValueError:
        return None


def feature_coordinates(feature: ArcGISFeature) -> tuple[float, float] | None:
    geometry = feature.geometry
    if geometry is None:
        return None
    if geometry.x is not None and geometry.y is not None:
        return geometry.y, geometry.x
    parts = geometry.rings or geometry.paths
    if not parts or not parts[0]:
        return None
    points = tuple(point for point in parts[0] if len(point) >= 2)
    if len(points) < 4:
        return None
    polygon = Polygon((point[0], point[1]) for point in points)
    if polygon.is_empty or not polygon.is_valid:
        return None
    centroid = polygon.centroid
    return centroid.y, centroid.x


def _require_approved_host(url: str) -> None:
    host = urlsplit(url).hostname or ""
    if host not in _ALLOWED_HOSTS:
        raise UnsupportedArcGISHostError(host=host)


def _raise_for_arcgis_error(content: bytes) -> None:
    envelope = ArcGISErrorEnvelope.model_validate_json(content)
    error = envelope.error
    if error is not None:
        raise ArcGISResponseError(
            code=error.code,
            message=error.message,
            details=error.details,
        )


async def get_arcgis_before_deadline(
    client: httpx.AsyncClient,
    url: str,
    *,
    params: dict[str, str | int | float],
    deadline: float,
) -> httpx.Response:
    _require_approved_host(url)
    remaining = deadline - anyio.current_time()
    if remaining <= 0:
        raise TimeoutError("County retrieval deadline exceeded.")
    with anyio.fail_after(remaining):
        return await client.get(url, params=params)


async def query_arcgis_features(
    client: httpx.AsyncClient,
    query: ArcGISQuery,
    *,
    deadline: float | None = None,
) -> ArcGISFeatureResult:
    """Fetch a bounded county spatial query using advertised pagination."""
    deadline = anyio.current_time() + 25 if deadline is None else deadline
    metadata_response = await get_arcgis_before_deadline(
        client, query.layer_url, params={"f": "json"}, deadline=deadline
    )
    metadata_response.raise_for_status()
    _raise_for_arcgis_error(metadata_response.content)
    metadata = ArcGISMetadata.model_validate_json(metadata_response.content)
    page_size = min(metadata.maxRecordCount, query.max_records)
    supports_pagination = metadata.advancedQueryCapabilities.supportsPagination
    object_id_field = (
        metadata.objectIdField
        or metadata.objectIdFieldName
        or next(
            (field.name for field in metadata.fields if field.type == "esriFieldTypeOID"),
            "",
        )
    )
    out_fields = query.out_fields
    if query.out_field_tails:
        out_fields = tuple(
            matches[0]
            for tail in query.out_field_tails
            if len(
                matches := tuple(
                    field.name for field in metadata.fields if field.name.rsplit(".", 1)[-1] == tail
                )
            )
            == 1
        )
    if object_id_field and object_id_field not in out_fields and "*" not in out_fields:
        out_fields = (*out_fields, object_id_field)
    features: list[ArcGISFeature] = []
    seen_records: dict[JsonScalar, list[ArcGISFeature]] = {}
    request_offset = 0
    exceeded = False
    repeated_page = False
    conflicting_records = False
    interrupted = False
    notes: list[str] = []

    while len(features) < query.max_records:
        remaining = query.max_records - len(features)
        params: dict[str, str | int | float] = {
            "f": "json",
            "where": query.where,
            "geometry": f"{query.longitude},{query.latitude}",
            "geometryType": "esriGeometryPoint",
            "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects",
            "distance": query.radius_miles,
            "units": "esriSRUnit_StatuteMile",
            "outFields": ",".join(out_fields),
            "returnGeometry": "true",
            "outSR": 4326,
        }
        if supports_pagination:
            params["resultOffset"] = request_offset
            params["resultRecordCount"] = min(page_size, remaining)
            if object_id_field:
                params["orderByFields"] = f"{object_id_field} ASC"
        try:
            response = await get_arcgis_before_deadline(
                client, f"{query.layer_url}/query", params=params, deadline=deadline
            )
            response.raise_for_status()
            _raise_for_arcgis_error(response.content)
            envelope = ArcGISFeatureEnvelope.model_validate_json(response.content)
        except (TimeoutError, httpx.HTTPError, ArcGISResponseError, ValidationError) as error:
            if not features:
                raise
            interrupted = True
            notes.append(
                f"County query interrupted by {type(error).__name__}; "
                f"{len(features)} completed records were retained. Coverage is incomplete."
            )
            break
        new_features: list[ArcGISFeature] = []
        for feature in envelope.features:
            object_id = feature.attributes.get(object_id_field) if object_id_field else None
            previous = seen_records.get(object_id, [])
            if previous:
                repeated_page = True
                if feature in previous:
                    continue
                conflicting_records = True
            if object_id is not None:
                seen_records.setdefault(object_id, []).append(feature)
            new_features.append(feature)
        features.extend(new_features[:remaining])
        request_offset += len(envelope.features)
        exceeded = envelope.exceededTransferLimit or len(new_features) > remaining
        if not supports_pagination or not exceeded or not envelope.features or not new_features:
            break

    partial = exceeded or repeated_page or interrupted
    if exceeded:
        notes.append(f"County response was truncated; {len(features)} records were retained.")
    if repeated_page:
        notes.append("County pagination repeated records; incomplete coverage is possible.")
    if conflicting_records:
        notes.append("County records sharing an object ID conflict; all variants require review.")
    return ArcGISFeatureResult(
        features=tuple(features),
        fields=metadata.fields,
        partial=partial,
        notes=tuple(notes),
    )
