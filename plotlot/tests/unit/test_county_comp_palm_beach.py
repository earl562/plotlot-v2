from __future__ import annotations

import httpx
import pytest
from pydantic import JsonValue

from plotlot.comps import CompPolicy, CompSubject
from plotlot.comps.arcgis import ArcGISFeature
from plotlot.comps.county_palm_beach import _map_feature, fetch_palm_beach_candidates


@pytest.mark.asyncio
async def test_palm_beach_keeps_price_with_sale_date_not_qualified_sale_date() -> None:
    # Given: a real-schema parcel where SALE_DATE and Q_SALE_DATE identify different days.
    fields = (
        ("OBJECTID", "esriFieldTypeOID"),
        ("PARID", "esriFieldTypeString"),
        ("PARCEL_NUMBER", "esriFieldTypeString"),
        ("SITE_ADDR_STR", "esriFieldTypeString"),
        ("SALEKEY", "esriFieldTypeInteger"),
        ("SALE_DATE", "esriFieldTypeDate"),
        ("BOOK", "esriFieldTypeString"),
        ("PAGE", "esriFieldTypeString"),
        ("PRICE", "esriFieldTypeString"),
        ("INSTRUMENT", "esriFieldTypeString"),
        ("QUAL_CODE", "esriFieldTypeString"),
        ("Q_SALE_DATE", "esriFieldTypeDate"),
        ("ACRES", "esriFieldTypeDouble"),
        ("PROPERTY_USE", "esriFieldTypeString"),
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/4"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 5000,
                    "objectIdField": "OBJECTID",
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [
                        {"name": name, "alias": name, "type": field_type}
                        for name, field_type in fields
                    ],
                },
            )
        return httpx.Response(
            200,
            json={
                "features": [
                    {
                        "attributes": {
                            "OBJECTID": 7,
                            "PARID": "00123456789000000",
                            "PARCEL_NUMBER": "00123456789000000",
                            "SITE_ADDR_STR": "7 TEST AVE",
                            "SALEKEY": 7654321,
                            "SALE_DATE": 1767571200000,
                            "BOOK": "12345",
                            "PAGE": "0678",
                            "PRICE": "450000",
                            "INSTRUMENT": "WD",
                            "QUAL_CODE": "QD",
                            "Q_SALE_DATE": 1735689600000,
                            "ACRES": 0.25,
                            "PROPERTY_USE": "SINGLE FAMILY",
                        },
                        "geometry": {
                            "rings": [
                                [
                                    [-80.25, 26.66],
                                    [-80.24, 26.66],
                                    [-80.24, 26.67],
                                    [-80.25, 26.67],
                                    [-80.25, 26.66],
                                ]
                            ]
                        },
                    }
                ],
                "exceededTransferLimit": False,
            },
        )

    subject = CompSubject(
        parcel_id="00999999999999999",
        state="FL",
        county="Palm Beach",
        latitude=26.66,
        longitude=-80.25,
        lot_size_sqft=10000,
    )
    policy = CompPolicy(as_of="2026-09-04")

    # When: the official Palm Beach adapter maps the parcel transaction.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_palm_beach_candidates(
            subject,
            policy,
            client=client,
            retrieved_at="2026-09-04T12:00:00Z",
        )

    # Then: current attributes and the unrelated qualified-sale date are not substituted.
    candidate = result.candidates[0]
    assert candidate.parcel_id == "00123456789000000"
    assert candidate.sale_date == "2026-01-05"
    assert candidate.sale_price == 450000.0
    assert candidate.qualification == "qualified"
    assert candidate.qualification_code == "QD"
    assert candidate.source_record_id == "7654321"
    assert candidate.recorded_document == "WD OR 12345/0678"
    assert candidate.property_type == "unknown"
    assert candidate.category == "unknown"
    assert candidate.lot_size_sqft is None
    assert any("at-sale" in note for note in result.notes)


@pytest.mark.asyncio
async def test_palm_beach_retains_valid_candidate_when_one_record_is_malformed() -> None:
    # Given: one valid feature and one with impossible WGS84 point geometry.
    fields = ("PARID", "SALEKEY", "SALE_DATE", "PRICE", "QUAL_CODE")

    def feature(parcel_id: str, latitude: float) -> dict[str, JsonValue]:
        return {
            "attributes": {
                "PARID": parcel_id,
                "SALEKEY": parcel_id,
                "SALE_DATE": 1767571200000,
                "PRICE": 450000,
                "QUAL_CODE": "Q",
            },
            "geometry": {"x": -80.25, "y": latitude},
        }

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/4"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 5000,
                    "advancedQueryCapabilities": {"supportsPagination": False},
                    "fields": [
                        {"name": name, "alias": name, "type": "esriFieldTypeString"}
                        for name in fields
                    ],
                },
            )
        return httpx.Response(
            200,
            json={"features": [feature("001", 26.66), feature("002", 999.0)]},
        )

    subject = CompSubject(
        parcel_id="009",
        state="FL",
        county="Palm Beach",
        latitude=26.66,
        longitude=-80.25,
        lot_size_sqft=6000,
    )

    # When: both records cross the county adapter boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_palm_beach_candidates(
            subject,
            CompPolicy(as_of="2026-09-04"),
            client=client,
        )

    # Then: the valid record survives and the malformed record is disclosed.
    assert tuple(candidate.parcel_id for candidate in result.candidates) == ("001",)
    assert result.status == "partial"
    assert any("malformed" in note for note in result.notes)


@pytest.mark.asyncio
@pytest.mark.parametrize("has_sale_key", [True, False])
async def test_palm_beach_keeps_condo_unit_sale_identity_when_map_parid_is_shared(
    has_sale_key: bool,
) -> None:
    # Given: two real county unit-sale rows share a map identifier, not a sale parcel.
    rows = (
        ("74434322400003000", "120 S OLIVE AVE 300", 3562401, 1777608000000, "300000"),
        ("74434322400003100", "120 S OLIVE AVE 310", 3531749, 1769144400000, "190000"),
    )
    attributes = [
        {
            "PARID": "7443432240",
            "PARCEL_NUMBER": parcel_number,
            "CONDO": "YES",
            "SITE_ADDR_STR": address,
            "SALEKEY": sale_key if has_sale_key else None,
            "SALE_DATE": sale_date,
            "PRICE": price,
            "QUAL_CODE": "Q",
        }
        for parcel_number, address, sale_key, sale_date, price in rows
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/4"):
            return httpx.Response(
                200,
                json={
                    "fields": [
                        {"name": name, "type": "esriFieldTypeString"} for name in attributes[0]
                    ]
                },
            )
        requested = request.url.params["outFields"].split(",")
        return httpx.Response(
            200,
            json={
                "features": [
                    {"attributes": {key: value for key, value in row.items() if key in requested}}
                    for row in attributes
                ]
            },
        )

    # When: the adapter queries and maps the official fields through its HTTP boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await fetch_palm_beach_candidates(
            CompSubject(
                parcel_id="subject",
                state="FL",
                county="Palm Beach",
                latitude=26.7132,
                longitude=-80.0513,
            ),
            CompPolicy(as_of="2026-09-05"),
            client=client,
        )

    # Then: unit sales stay distinct without inventing at-sale property characteristics.
    assert tuple((row.parcel_id, row.sale_price, row.sale_date) for row in result.candidates) == (
        ("74434322400003000", 300000.0, "2026-05-01"),
        ("74434322400003100", 190000.0, "2026-01-23"),
    )
    assert len({row.evidence_id for row in result.candidates}) == 2
    for candidate in result.candidates:
        assert candidate.conflict_flags == ()
        assert "7443432240" in candidate.review_notes
        assert candidate.category == "unknown"
        assert candidate.property_type == "unknown"
        assert candidate.lot_size_sqft is None


@pytest.mark.parametrize(
    "condo,parcel_number",
    [
        ("NO", "74434322400003000"),
        (None, "74434322400003000"),
        ("UNKNOWN", "74434322400003000"),
        ("YES", "99934322400003000"),
        ("YES", "7443432240000300"),
        ("YES", "7443432240000300X"),
    ],
)
def test_palm_beach_keeps_unexplained_parcel_mismatches_for_review(
    condo: str | None,
    parcel_number: str,
) -> None:
    # Given: absent condo evidence or a unit ID outside the observed map hierarchy.
    feature = ArcGISFeature(
        attributes={
            "PARID": "7443432240",
            "PARCEL_NUMBER": parcel_number,
            "CONDO": condo,
        }
    )
    # When: the real county mapper interprets the identity evidence.
    candidate = _map_feature(feature, "2026-09-05T12:00:00Z")
    # Then: the mismatch remains visible and disqualifying for human review.
    assert candidate.conflict_flags == ("parcel_identifier_mismatch",)
