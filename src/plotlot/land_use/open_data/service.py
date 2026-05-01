"""Open-data/geospatial service wrappers returning cited layer candidates."""

from __future__ import annotations

from typing import cast

from pydantic import HttpUrl, TypeAdapter

from plotlot.land_use.citations import arcgis_layer_citation
from plotlot.land_use.models import EvidenceConfidence, LayerCandidate, LayerType
from plotlot.property.hub_discovery import discover_datasets


_HTTP_URL = TypeAdapter(HttpUrl)
_LAYER_TYPES: set[str] = {
    "parcel",
    "zoning",
    "land_use",
    "utility",
    "environment",
    "transportation",
    "economic_development",
    "unknown",
}


async def discover_layers(*, county: str, state: str, lat: float, lng: float):
    parcels, zoning = await discover_datasets(county=county, state=state, lat=lat, lng=lng)

    candidates: list[LayerCandidate] = []
    for ds in [parcels, zoning]:
        if not ds:
            continue

        try:
            source_url = _HTTP_URL.validate_python(ds.url)
            service_url_str = f"{ds.url}/{ds.layer_id}" if ds.layer_id is not None else ds.url
            service_url = _HTTP_URL.validate_python(service_url_str)
        except Exception:
            # Skip invalid URLs rather than returning malformed candidates.
            continue

        layer_type: LayerType
        if ds.dataset_type in _LAYER_TYPES:
            layer_type = cast(LayerType, ds.dataset_type)
        else:
            layer_type = "unknown"

        citation = arcgis_layer_citation(
            title=ds.name,
            service_url=service_url_str,
            jurisdiction=f"{county}, {state}",
            raw_text_for_hash=f"{ds.dataset_id}:{ds.url}:{ds.layer_id}:{','.join(ds.fields)}",
        )
        candidates.append(
            LayerCandidate(
                id=ds.dataset_id,
                title=ds.name,
                source_url=source_url,
                service_url=service_url,
                layer_id=ds.layer_id or 0,
                layer_type=layer_type,
                field_mapping_confidence=EvidenceConfidence.MEDIUM,
                citation=citation,
            )
        )
    return candidates
