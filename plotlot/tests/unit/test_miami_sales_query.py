from contextlib import closing
import sqlite3

import httpx
import pytest

from plotlot.comps import CompPolicy, CompSubject
from plotlot.comps.county_miami_dade import fetch_miami_dade_candidates


@pytest.mark.parametrize(
    ("policy", "bounds"),
    [
        (CompPolicy(as_of="2026-09-14", months=12), ("20250914", "20250913")),
        (CompPolicy(as_of="2024-03-31", months=1), ("20240229", "20240228")),
        (CompPolicy(as_of="2026-01-15", months=2), ("20251115", "20251114")),
    ],
)
@pytest.mark.parametrize("land", [True, False], ids=["land", "resale"])
async def test_recent_sales_are_not_crowded_out_by_old_parcels(
    policy: CompPolicy, bounds: tuple[str, str], land: bool
) -> None:
    cutoff, older = bounds
    as_of = policy.as_of
    # Given: an official-shaped service with more old parcels than the retrieval cap.
    columns = ("OBJECTID", "FOLIO", "DOS_1", "VI_1", "DOS_2", "VI_2", "DOS_3", "VI_3")
    metadata_fields = (
        *columns,
        *(f"{prefix}_{slot}" for prefix in ("PRICE", "QU_FLG") for slot in (1, 2, 3)),
    )
    with closing(sqlite3.connect(":memory:")) as database:
        database.row_factory = sqlite3.Row
        database.execute(
            "CREATE TABLE parcels (OBJECTID INTEGER, FOLIO TEXT, DOS_1 TEXT, VI_1 TEXT, "
            "DOS_2 TEXT, VI_2 TEXT, DOS_3 TEXT, VI_3 TEXT)"
        )
        database.executemany(
            "INSERT INTO parcels VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [(i, f"SYNTHETIC-OLD-{i}", older, "V", None, None, None, None) for i in range(1001)],
        )
        database.executemany(
            "INSERT INTO parcels VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                (1001, "SYNTHETIC-LOWER", cutoff, "V", None, None, None, None),
                (1002, "SYNTHETIC-UPPER", None, None, as_of.replace("-", ""), "V", None, None),
                (1003, "SYNTHETIC-THIRD", None, None, None, None, cutoff, "V"),
                (1004, "SYNTHETIC-CROSS-SLOT", older, "V", cutoff, "I", None, None),
                (1005, "SYNTHETIC-FUTURE", "20990101", "V", None, None, None, None),
            ],
        )

        def handler(request: httpx.Request) -> httpx.Response:
            if not request.url.path.endswith("/query"):
                return httpx.Response(
                    200,
                    json={
                        "maxRecordCount": 20000,
                        "objectIdField": "OBJECTID",
                        "advancedQueryCapabilities": {"supportsPagination": True},
                        "fields": [
                            {"name": name, "type": "esriFieldTypeString"}
                            for name in metadata_fields
                        ],
                    },
                )
            where = request.url.params["where"]
            count = int(request.url.params["resultRecordCount"])
            offset = int(request.url.params["resultOffset"])
            rows = database.execute(
                f"SELECT * FROM parcels WHERE {where} ORDER BY OBJECTID LIMIT ? OFFSET ?",
                (count + 1, offset),
            ).fetchall()
            return httpx.Response(
                200,
                json={
                    "features": [
                        {
                            "attributes": dict(row),
                            "geometry": {"x": -80.19, "y": 25.77},
                        }
                        for row in rows[:count]
                    ],
                    "exceededTransferLimit": len(rows) > count,
                },
            )

        subject = CompSubject(
            parcel_id="SYNTHETIC-SUBJECT",
            state="FL",
            county="Miami-Dade",
            latitude=25.77,
            longitude=-80.19,
            category="land" if land else "resale",
            property_type="land" if land else "single_family",
        )
        # When: the actual adapter sends its policy-bound query through the HTTP boundary.
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            result = await fetch_miami_dade_candidates(subject, policy, client=client)

    # Then: relevant slots at both inclusive date boundaries survive without truncation.
    expected = {"SYNTHETIC-LOWER", "SYNTHETIC-UPPER", "SYNTHETIC-THIRD"}
    if not land:
        expected.add("SYNTHETIC-CROSS-SLOT")
    assert {sale.parcel_id for sale in result.candidates} == expected
    assert result.status == "available"
    assert all(sale.lot_size_sqft is None for sale in result.candidates)
