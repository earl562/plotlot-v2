from __future__ import annotations

import httpx
import pytest
from pydantic import JsonValue

from plotlot.comps import CompPolicy, CompSubject
from plotlot.comps.county_miami_dade import fetch_miami_dade_candidates


@pytest.mark.asyncio
async def test_miami_dade_keeps_three_transaction_slots_paired() -> None:
    # Given: one real-schema parcel whose second and third sale slots are complementary.
    requested_record_counts: list[str] = []
    field_names = (
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
        "LOT_SIZE",
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/5"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 20_000,
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [
                        {"name": name, "alias": name.lower(), "type": "esriFieldTypeString"}
                        for name in field_names
                    ],
                },
            )
        requested_record_counts.append(request.url.params["resultRecordCount"])
        return httpx.Response(
            200,
            json={
                "features": [
                    {
                        "attributes": {
                            "FOLIO": "0012345678900",
                            "TRUE_SITE_ADDR": "1 TEST ST",
                            "DOS_1": "20260105",
                            "OR_BK_1": "12345",
                            "OR_PG_1": "0067",
                            "PRICE_1": 400000,
                            "QU_FLG_1": "Q",
                            "VI_1": "V",
                            "DOS_2": "20250102",
                            "OR_BK_2": "",
                            "OR_PG_2": "",
                            "PRICE_2": None,
                            "QU_FLG_2": "U",
                            "VI_2": "I",
                            "DOS_3": None,
                            "OR_BK_3": "99999",
                            "OR_PG_3": "0001",
                            "PRICE_3": 900000,
                            "QU_FLG_3": "Q",
                            "VI_3": "I",
                            "LOT_SIZE": 5000,
                        },
                        "geometry": {"x": -80.19, "y": 25.75},
                    }
                ],
                "exceededTransferLimit": False,
            },
        )

    subject = CompSubject(
        parcel_id="0099999999999",
        state="FL",
        county="Miami-Dade",
        latitude=25.75,
        longitude=-80.19,
        lot_size_sqft=6000,
    )
    policy = CompPolicy(as_of="2026-09-04")

    # When: the official Miami-Dade adapter maps the parcel response.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_miami_dade_candidates(
            subject,
            policy,
            client=client,
            retrieved_at="2026-09-04T12:00:00Z",
        )

    # Then: no date, price, or current parcel area crosses between transaction slots.
    assert tuple((sale.sale_date, sale.sale_price) for sale in result.candidates) == (
        ("2026-01-05", 400000.0),
        ("2025-01-02", None),
        ("", 900000.0),
    )
    assert requested_record_counts == ["1000"]
    assert result.candidates[0].date_precision == "day"
    assert result.candidates[0].category == "land"
    assert result.candidates[0].recorded_document == "OR 12345/0067"
    assert result.candidates[0].lot_size_sqft is None
    assert result.candidates[1].category == "unknown"
    assert result.candidates[2].sale_date == ""
    assert any("at-sale lot size" in note for note in result.notes)


@pytest.mark.asyncio
async def test_miami_dade_refuses_mapping_when_metadata_lacks_transaction_fields() -> None:
    # Given: a county metadata response missing the canonical PRICE_1 field.
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/5"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 20_000,
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [
                        {"name": "FOLIO", "alias": "folio", "type": "esriFieldTypeString"},
                        {"name": "DOS_1", "alias": "dos_1", "type": "esriFieldTypeString"},
                    ],
                },
            )
        return httpx.Response(200, json={"features": []})

    subject = CompSubject(
        parcel_id="0099999999999",
        state="FL",
        county="Miami-Dade",
        latitude=25.75,
        longitude=-80.19,
        lot_size_sqft=6000,
    )

    # When: the adapter sees schema drift at the official metadata boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_miami_dade_candidates(
            subject,
            CompPolicy(as_of="2026-09-04"),
            client=client,
        )

    # Then: schema drift is unavailable evidence, not a silent zero-sale result.
    assert result.status == "unavailable"
    assert result.candidates == ()
    assert "PRICE_1" in result.notes[0]


@pytest.mark.asyncio
async def test_miami_dade_retains_valid_candidates_when_one_record_is_malformed() -> None:
    # Given: one valid sale and one county feature with impossible WGS84 geometry.
    required_fields = (
        "FOLIO",
        *(f"{prefix}_{slot}" for prefix in ("DOS", "PRICE", "QU_FLG", "VI") for slot in (1, 2, 3)),
    )

    def feature(folio: str, latitude: float) -> dict[str, JsonValue]:
        return {
            "attributes": {
                "FOLIO": folio,
                "DOS_1": "20260105",
                "PRICE_1": 400000,
                "QU_FLG_1": "Q",
                "VI_1": "V",
                "DOS_2": None,
                "PRICE_2": None,
                "QU_FLG_2": None,
                "VI_2": None,
                "DOS_3": None,
                "PRICE_3": None,
                "QU_FLG_3": None,
                "VI_3": None,
            },
            "geometry": {"x": -80.19, "y": latitude},
        }

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/5"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 20_000,
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [
                        {"name": name, "alias": name, "type": "esriFieldTypeString"}
                        for name in required_fields
                    ],
                },
            )
        return httpx.Response(
            200,
            json={"features": [feature("001", 25.75), feature("002", 999.0)]},
        )

    subject = CompSubject(
        parcel_id="009",
        state="FL",
        county="Miami-Dade",
        latitude=25.75,
        longitude=-80.19,
        lot_size_sqft=6000,
    )

    # When: both features cross the county adapter boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_miami_dade_candidates(
            subject,
            CompPolicy(as_of="2026-09-04"),
            client=client,
        )

    # Then: the valid sale remains visible and the malformed record makes coverage partial.
    assert tuple(candidate.parcel_id for candidate in result.candidates) == ("001",)
    assert result.status == "partial"
    assert any("malformed" in note for note in result.notes)
