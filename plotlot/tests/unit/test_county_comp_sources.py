from __future__ import annotations

import pytest

from plotlot.comps import CompPolicy, CompSubject
from plotlot.comps.sources import fetch_county_candidates


@pytest.mark.asyncio
async def test_fetch_county_candidates_marks_san_diego_unsupported() -> None:
    # Given: a San Diego subject where no automated official price source is approved.
    subject = CompSubject(
        parcel_id="1234567890",
        state="CA",
        county="San Diego",
        latitude=32.72,
        longitude=-117.16,
        lot_size_sqft=5000,
    )
    policy = CompPolicy(as_of="2026-09-04")

    # When: the official-source dispatcher is called.
    result = await fetch_county_candidates(subject, policy)

    # Then: it abstains and directs the caller to reviewed evidence imports.
    assert result.status == "unsupported"
    assert result.candidates == ()
    assert "human-reviewed" in result.notes[0]
    assert result.source_urls == ()
