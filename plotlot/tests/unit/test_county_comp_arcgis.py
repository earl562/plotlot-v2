from __future__ import annotations

import json

import httpx
import pytest

from plotlot.comps.arcgis import (
    ArcGISFeature,
    ArcGISQuery,
    ArcGISResponseError,
    feature_coordinates,
    parse_arcgis_day,
    query_arcgis_features,
)


@pytest.mark.asyncio
async def test_query_arcgis_features_collects_bounded_pages_when_supported() -> None:
    # Given: a layer that advertises two-record pagination and has three records.
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/5"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 2,
                    "objectIdField": "OBJECTID",
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [
                        {"name": "OBJECTID", "alias": "OBJECTID", "type": "esriFieldTypeOID"},
                        {"name": "FOLIO", "alias": "folio", "type": "esriFieldTypeString"},
                    ],
                },
            )
        offset = int(request.url.params.get("resultOffset", "0"))
        features = {
            0: [
                {"attributes": {"OBJECTID": 1, "FOLIO": "001"}},
                {"attributes": {"OBJECTID": 2, "FOLIO": "002"}},
            ],
            2: [{"attributes": {"OBJECTID": 3, "FOLIO": "003"}}],
        }[offset]
        return httpx.Response(
            200,
            content=json.dumps(
                {
                    "features": features,
                    "exceededTransferLimit": offset == 0,
                }
            ),
        )

    query = ArcGISQuery(
        layer_url=(
            "https://gisweb.miamidade.gov/arcgis/rest/services/MD_ComparableSales/MapServer/5"
        ),
        latitude=25.75,
        longitude=-80.19,
        radius_miles=3,
        out_fields=("OBJECTID", "FOLIO"),
        max_records=3,
    )

    # When: the bounded spatial query is executed through the HTTP boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await query_arcgis_features(client, query)

    # Then: both pages are returned without claiming partial coverage.
    assert tuple(feature.attributes["FOLIO"] for feature in result.features) == (
        "001",
        "002",
        "003",
    )
    assert result.partial is False
    assert result.notes == ()


@pytest.mark.asyncio
async def test_query_arcgis_features_raises_typed_error_for_arcgis_error_envelope() -> None:
    # Given: a county layer that returns HTTP 200 with an ArcGIS error envelope.
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/5"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 20_000,
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [],
                },
            )
        return httpx.Response(
            200,
            json={"error": {"code": 400, "message": "Invalid field", "details": []}},
        )

    query = ArcGISQuery(
        layer_url=(
            "https://gisweb.miamidade.gov/arcgis/rest/services/MD_ComparableSales/MapServer/5"
        ),
        latitude=25.75,
        longitude=-80.19,
        radius_miles=3,
        out_fields=("FOLIO",),
        max_records=5,
    )

    # When: the error response crosses the HTTP boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        with pytest.raises(ArcGISResponseError) as captured:
            await query_arcgis_features(client, query)

    # Then: the county error remains explicit instead of becoming an empty result.
    assert captured.value.code == 400
    assert captured.value.message == "Invalid field"


def test_parse_arcgis_day_distinguishes_numeric_yyyymmdd_from_epoch_milliseconds() -> None:
    # Given: county dates encoded in the two numeric formats used by the official layers.
    numeric_day = 20260105
    epoch_milliseconds = 1767571200000

    # When: both values cross the ArcGIS date boundary.
    results = (parse_arcgis_day(numeric_day), parse_arcgis_day(epoch_milliseconds))

    # Then: both retain the same exact calendar day without a 1970 conversion.
    assert results == ("2026-01-05", "2026-01-05")


@pytest.mark.asyncio
async def test_query_arcgis_features_marks_unpageable_truncation_partial() -> None:
    # Given: a Broward-style layer that cannot paginate but reports more records.
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/17"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 1000,
                    "advancedQueryCapabilities": {"supportsPagination": False},
                    "fields": [],
                },
            )
        return httpx.Response(
            200,
            json={
                "features": [{"attributes": {"id": 1}}],
                "exceededTransferLimit": True,
            },
        )

    query = ArcGISQuery(
        layer_url=(
            "https://gisweb-adapters.bcpa.net/arcgis/rest/services/BCPA_EXTERNAL_JAN26/MapServer/17"
        ),
        latitude=26.10,
        longitude=-80.10,
        radius_miles=3,
        out_fields=("*",),
    )

    # When: the unpageable layer returns its bounded first response.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await query_arcgis_features(client, query)

    # Then: the response is retained but incomplete coverage is explicit.
    assert len(result.features) == 1
    assert result.partial is True
    assert "truncated" in result.notes[0].lower()


def test_feature_coordinates_uses_polygon_centroid_instead_of_vertex_average() -> None:
    # Given: an asymmetric closed parcel ring where vertex averaging is biased.
    feature = ArcGISFeature(
        attributes={},
        geometry={
            "rings": [
                [
                    [0.0, 0.0],
                    [4.0, 0.0],
                    [4.0, 1.0],
                    [1.0, 1.0],
                    [1.0, 4.0],
                    [0.0, 4.0],
                    [0.0, 0.0],
                ]
            ]
        },
    )

    # When: the representative coordinate is derived from official geometry.
    coordinates = feature_coordinates(feature)

    # Then: the coordinate matches the polygon centroid, not the mean of vertices.
    assert coordinates == pytest.approx((1.3571428571, 1.3571428571))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "oid_metadata", ["objectIdField", "objectIdFieldName", "field_type", "field_tails"]
)
@pytest.mark.parametrize(
    ("second_rows", "expected_values", "explicit_oid"),
    [
        ([(1, 100), (2, 200)], (100, 200), False),
        ([(2, 200), (3, 300)], (100, 200, 300), False),
        ([(2, 250), (3, 300)], (100, 200, 250, 300), True),
    ],
    ids=["repeated-page", "overlapping-page", "conflicting-record"],
)
async def test_query_arcgis_features_preserves_evidence_when_pages_overlap(
    oid_metadata: str,
    second_rows: list[tuple[int, int]],
    expected_values: tuple[int, ...],
    explicit_oid: bool,
) -> None:
    # Given: limited fields and overlapping county pages, including a changed price.
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/4"):
            return httpx.Response(
                200,
                json={
                    "maxRecordCount": 2,
                    **({oid_metadata: "OBJECTID"} if oid_metadata != "field_type" else {}),
                    "advancedQueryCapabilities": {"supportsPagination": True},
                    "fields": [
                        {"name": "OBJECTID", "alias": "OBJECTID", "type": "esriFieldTypeOID"},
                        {"name": "VALUE", "type": "esriFieldTypeDouble"},
                    ],
                },
            )
        offset = int(request.url.params.get("resultOffset", "0"))
        assert offset in (0, 2)
        rows = [(1, 100), (2, 200)] if offset == 0 else second_rows
        requested_fields = request.url.params["outFields"].split(",")
        return httpx.Response(
            200,
            json={
                "features": [
                    {
                        "attributes": {
                            key: value
                            for key, value in {"OBJECTID": oid, "VALUE": price}.items()
                            if key in requested_fields
                        }
                    }
                    for oid, price in rows
                ],
                "exceededTransferLimit": offset == 0 or len(expected_values) == 2,
            },
        )

    query = ArcGISQuery(
        layer_url=(
            "https://gis.pbcgov.org/arcgis/rest/services/Parcels/PARCEL_INFO/FeatureServer/4"
        ),
        latitude=26.66,
        longitude=-80.25,
        radius_miles=3,
        out_fields=("OBJECTID", "VALUE") if explicit_oid else ("VALUE",),
        out_field_tails=("VALUE",) if oid_metadata == "field_tails" else (),
        max_records=5,
    )

    # When: the repeated second page crosses the pagination boundary.
    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        result = await query_arcgis_features(client, query)

    # Then: exact repeats disappear, but conflicting evidence remains for review.
    assert tuple(feature.attributes["VALUE"] for feature in result.features) == expected_values
    assert all("OBJECTID" in feature.attributes for feature in result.features)
    assert result.partial is True
    assert any("repeated" in note.lower() for note in result.notes)
    if explicit_oid:
        assert any("conflict" in note.lower() for note in result.notes)


def test_arcgis_model_types_remain_available_from_public_module() -> None:
    from plotlot.comps import arcgis, arcgis_models

    for name in (
        "JsonScalar",
        "UnsupportedArcGISHostError",
        "ArcGISResponseError",
        "ArcGISErrorPayload",
        "ArcGISErrorEnvelope",
        "ArcGISField",
        "ArcGISAdvancedCapabilities",
        "ArcGISMetadata",
        "ArcGISGeometry",
        "ArcGISFeature",
        "ArcGISFeatureEnvelope",
        "ArcGISQuery",
        "ArcGISFeatureResult",
    ):
        assert getattr(arcgis, name) is getattr(arcgis_models, name)
