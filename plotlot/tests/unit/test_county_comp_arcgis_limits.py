from __future__ import annotations

import httpx
import pytest

from plotlot.comps.arcgis import ArcGISQuery, query_arcgis_features


@pytest.mark.asyncio
@pytest.mark.parametrize("supports_pagination", [False, True])
@pytest.mark.parametrize(
    ("max_records", "expected_ids", "expected_partial"),
    [(2, (1, 2), True), (3, (1, 2, 3), False)],
    ids=["locally-clipped", "complete-at-local-cap"],
)
async def test_local_record_limit_reports_discarded_county_evidence(
    supports_pagination: bool,
    max_records: int,
    expected_ids: tuple[int, ...],
    expected_partial: bool,
) -> None:
    # Given: a complete county response may be larger than PlotLot's local cap.
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/17"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 1000,
                    "objectIdField": "OBJECTID",
                    "advancedQueryCapabilities": {"supportsPagination": supports_pagination},
                    "fields": [{"name": "OBJECTID", "type": "esriFieldTypeOID"}],
                },
            )
        return httpx.Response(
            200,
            json={
                "features": [{"attributes": {"OBJECTID": value}} for value in (1, 2, 3)],
                "exceededTransferLimit": False,
            },
        )

    query = ArcGISQuery(
        layer_url=(
            "https://gisweb-adapters.bcpa.net/arcgis/rest/services/BCPA_EXTERNAL_JAN26/MapServer/17"
        ),
        latitude=26.129416339055034,
        longitude=-80.13317364345802,
        radius_miles=0.25,
        out_fields=("OBJECTID",),
        max_records=max_records,
    )

    # When: the real query implementation applies its local retention limit.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await query_arcgis_features(client, query)

    # Then: only actual local clipping changes the completeness outcome.
    assert tuple(feature.attributes["OBJECTID"] for feature in result.features) == expected_ids
    assert result.partial is expected_partial
    assert bool(result.notes) is expected_partial
