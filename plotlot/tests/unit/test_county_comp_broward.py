from __future__ import annotations

import httpx
import pytest

from plotlot.comps import CompPolicy, CompSubject
from plotlot.comps.county_broward import fetch_broward_candidates


@pytest.mark.asyncio
async def test_broward_discovers_2025_and_2026_sales_by_metadata_name() -> None:
    # Given: the pinned BCPA service contains year layers and similarly named group layers.
    requested_query_layers: list[str] = []
    requested_out_fields: list[str] = []
    field_names = (
        "SQLGIS02.DATALAYER.Parcel_Polygons.OBJECTID",
        "SQLGIS02.DATALAYER.Parcel_Polygons.FOLIO",
        "SQLGIS02.dbo.BCPA_SALES.FOLIO_NUMBER",
        "SQLGIS02.dbo.BCPA_SALES.SALE_DATE",
        "SQLGIS02.dbo.BCPA_SALES.SALE_AMOUNT",
        "SQLGIS02.dbo.BCPA_SALES.SALE_VER",
        "SQLGIS02.dbo.BCPA_SALES.SALE_YEAR",
    )

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/MapServer"):
            return httpx.Response(
                200,
                json={
                    "layers": [
                        {"id": 17, "name": "2026 Sales"},
                        {"id": 18, "name": "2025 Sales"},
                        {"id": 19, "name": "2024 Sales"},
                        {"id": 20, "name": "2026 Sales Group"},
                    ]
                },
            )
        if path.endswith(("/17", "/18", "/19", "/20")):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 1000,
                    "advancedQueryCapabilities": {"supportsPagination": False},
                    "fields": [
                        {
                            "name": name,
                            "alias": name.rsplit(".", 1)[-1],
                            "type": (
                                "esriFieldTypeOID"
                                if name.endswith("OBJECTID")
                                else "esriFieldTypeString"
                            ),
                        }
                        for name in field_names
                    ],
                },
            )
        layer = path.rsplit("/", 2)[-2]
        requested_query_layers.append(layer)
        requested_out_fields.append(request.url.params["outFields"])
        sale_year = {"17": 2026, "18": 2025}[layer]
        return httpx.Response(
            200,
            json={
                "features": [
                    {
                        "attributes": {
                            field_names[0]: sale_year,
                            field_names[1]: f"00{sale_year}",
                            field_names[2]: f"00{sale_year}",
                            field_names[3]: 1767225600000 if sale_year == 2026 else 1735689600000,
                            field_names[4]: f"${sale_year:,}",
                            field_names[5]: "Q" if sale_year == 2026 else "U",
                            field_names[6]: str(sale_year),
                        },
                        "geometry": {
                            "rings": [
                                [
                                    [-80.10, 26.10],
                                    [-80.11, 26.10],
                                    [-80.11, 26.11],
                                    [-80.10, 26.10],
                                ]
                            ]
                        },
                    }
                ]
            },
        )

    subject = CompSubject(
        parcel_id="009999999999",
        state="FL",
        county="Broward",
        latitude=26.10,
        longitude=-80.10,
        lot_size_sqft=6000,
    )
    policy = CompPolicy(as_of="2026-09-04", months=12)

    # When: Broward candidates are fetched through the pinned service.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_broward_candidates(
            subject,
            policy,
            client=client,
            retrieved_at="2026-09-04T12:00:00Z",
        )

    # Then: only the intersecting exact year layers contribute evidence.
    assert requested_query_layers == ["17", "18"]
    assert all(value != "*" for value in requested_out_fields)
    assert all("SALE_AMOUNT" in value for value in requested_out_fields)
    assert tuple(candidate.sale_date for candidate in result.candidates) == (
        "2026-01-01",
        "2025-01-01",
    )
    assert tuple(candidate.qualification for candidate in result.candidates) == (
        "qualified",
        "disqualified",
    )
    assert all(candidate.category == "unknown" for candidate in result.candidates)
    assert all(candidate.lot_size_sqft is None for candidate in result.candidates)
    assert result.status == "available"


@pytest.mark.asyncio
async def test_broward_retains_earlier_layer_when_later_layer_has_schema_drift() -> None:
    # Given: 2026 maps cleanly while the 2025 layer omits its canonical sale-price field.
    good_fields = (
        "SQLGIS02.DATALAYER.Parcel_Polygons.OBJECTID",
        "SQLGIS02.DATALAYER.Parcel_Polygons.FOLIO",
        "SQLGIS02.dbo.BCPA_SALES.FOLIO_NUMBER",
        "SQLGIS02.dbo.BCPA_SALES.SALE_DATE",
        "SQLGIS02.dbo.BCPA_SALES.SALE_AMOUNT",
        "SQLGIS02.dbo.BCPA_SALES.SALE_VER",
    )

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/MapServer"):
            return httpx.Response(
                200,
                json={
                    "layers": [
                        {"id": 17, "name": "2026 Sales"},
                        {"id": 18, "name": "2025 Sales"},
                    ]
                },
            )
        if path.endswith(("/17", "/18")):
            fields = (
                good_fields
                if path.endswith("/17")
                else tuple(name for name in good_fields if not name.endswith("SALE_AMOUNT"))
            )
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 1000,
                    "advancedQueryCapabilities": {"supportsPagination": False},
                    "fields": [
                        {
                            "name": name,
                            "alias": name.rsplit(".", 1)[-1],
                            "type": "esriFieldTypeString",
                        }
                        for name in fields
                    ],
                },
            )
        if "/17/query" in path:
            return httpx.Response(
                200,
                json={
                    "features": [
                        {
                            "attributes": {
                                good_fields[0]: 17,
                                good_fields[1]: "001",
                                good_fields[2]: "001",
                                good_fields[3]: 1767225600000,
                                good_fields[4]: 450000,
                                good_fields[5]: "Q",
                            },
                            "geometry": {"x": -80.1, "y": 26.1},
                        }
                    ]
                },
            )
        return httpx.Response(200, json={"features": [{"attributes": {}}]})

    subject = CompSubject(
        parcel_id="009",
        state="FL",
        county="Broward",
        latitude=26.1,
        longitude=-80.1,
        lot_size_sqft=6000,
    )

    # When: both year layers cross the official metadata boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_broward_candidates(
            subject,
            CompPolicy(as_of="2026-09-04", months=12),
            client=client,
        )

    # Then: the valid year remains visible and schema drift makes coverage partial.
    assert tuple(candidate.parcel_id for candidate in result.candidates) == ("001",)
    assert result.status == "partial"
    assert any("2025 metadata lacks" in note for note in result.notes)


@pytest.mark.asyncio
async def test_broward_reports_timeout_type_when_httpx_message_is_empty() -> None:
    # Given: the official service times out with an empty exception message.
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("", request=request)

    subject = CompSubject(
        parcel_id="009",
        state="FL",
        county="Broward",
        latitude=26.1,
        longitude=-80.1,
        lot_size_sqft=6000,
    )

    # When: the adapter handles the typed transport failure.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_broward_candidates(
            subject,
            CompPolicy(as_of="2026-09-04"),
            client=client,
        )

    # Then: operators can see what failed even when httpx supplies no message.
    assert result.status == "unavailable"
    assert "ReadTimeout" in result.notes[-1]
