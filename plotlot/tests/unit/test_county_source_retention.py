from __future__ import annotations

from unittest.mock import patch

import anyio
import httpx
import pytest

from plotlot.comps import CompPolicy, CompSubject
from plotlot.comps.arcgis import ArcGISQuery, query_arcgis_features
from plotlot.comps.county_broward import BROWARD_SERVICE_URL, fetch_broward_candidates
from plotlot.comps.county_miami_dade import fetch_miami_dade_candidates
from plotlot.comps.county_palm_beach import fetch_palm_beach_candidates


@pytest.mark.parametrize("failure", ["timeout", "http", "arcgis", "malformed"])
async def test_completed_arcgis_page_survives_later_page_failure(failure: str) -> None:
    # Given: one completed official page followed by an unsuccessful second page.
    def handler(request: httpx.Request) -> httpx.Response:
        if not request.url.path.endswith("/query"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 1,
                    "objectIdField": "OBJECTID",
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [{"name": "OBJECTID", "type": "esriFieldTypeOID"}],
                },
            )
        if request.url.params["resultOffset"] == "0":
            return httpx.Response(
                200,
                json={
                    "features": [{"attributes": {"OBJECTID": 1, "PRICE": 200000}}],
                    "exceededTransferLimit": True,
                },
            )
        assert request.url.params["resultOffset"] == "1"
        if failure == "timeout":
            raise httpx.ReadTimeout("second page stalled", request=request)
        if failure == "http":
            return httpx.Response(503)
        if failure == "arcgis":
            return httpx.Response(200, json={"error": {"code": 500, "message": "query failed"}})
        return httpx.Response(200, content=b"not-json")

    # When: the shared query crosses the real HTTPX parsing and pagination boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await query_arcgis_features(
            client,
            ArcGISQuery(
                layer_url=f"{BROWARD_SERVICE_URL}/17",
                latitude=26.1,
                longitude=-80.1,
                radius_miles=3,
                out_fields=("OBJECTID", "PRICE"),
            ),
        )

    # Then: completed evidence remains inspectable but coverage is explicitly incomplete.
    assert tuple(feature.attributes["PRICE"] for feature in result.features) == (200000,)
    assert result.partial is True
    assert any("interrupted" in note.lower() for note in result.notes)


@pytest.mark.parametrize("county", ["Broward", "Miami-Dade", "Palm Beach"])
@pytest.mark.parametrize("owned", [True, False], ids=["owned", "borrowed"])
async def test_caller_cancellation_propagates_and_only_owned_client_is_closed(
    county: str,
    owned: bool,
) -> None:
    # Given: cancellation interrupts a real client request and closing needs an async checkpoint.
    close_finished = False
    returned_result = False

    class ClosingTransport(httpx.MockTransport):
        async def aclose(self) -> None:
            nonlocal close_finished
            await anyio.lowlevel.checkpoint()
            close_finished = True

    async def handler(request: httpx.Request) -> httpx.Response:
        caller.cancel()
        await anyio.sleep_forever()
        raise AssertionError("unreachable")

    fetch = {
        "Broward": fetch_broward_candidates,
        "Miami-Dade": fetch_miami_dade_candidates,
        "Palm Beach": fetch_palm_beach_candidates,
    }[county]
    client = httpx.AsyncClient(transport=ClosingTransport(handler))

    # When: the caller cancels, without the county's own deadline expiring.
    try:
        with patch("httpx.AsyncClient", return_value=client), anyio.CancelScope() as caller:
            await fetch(
                CompSubject(
                    parcel_id="009", state="FL", county=county, latitude=26.1, longitude=-80.1
                ),
                CompPolicy(as_of="2026-09-07"),
                client=None if owned else client,
            )
            returned_result = True

        # Then: cancellation escapes and owned cleanup completes without closing borrowed resources.
        assert caller.cancelled_caught
        assert returned_result is False
        assert close_finished is owned
        assert client.is_closed is owned
    finally:
        await client.aclose()
