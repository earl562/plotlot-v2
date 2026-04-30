"""Unit tests for evidence/report/document read APIs."""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest


@pytest.mark.asyncio
async def test_list_evidence_returns_rows(client):
    from plotlot.storage.models import EvidenceItem

    ev = EvidenceItem(
        id="ev_1",
        workspace_id="ws_1",
        project_id="prj_1",
        claim_key="x",
        value_json={"a": 1},
        source_type="ordinance",
        tool_name="search_zoning_ordinance",
        confidence="medium",
        metadata_json={},
        retrieved_at=datetime(2026, 4, 30, 12, 0, tzinfo=timezone.utc),
    )

    class _Rows:
        def all(self):
            return [ev]

    class _Result:
        def scalars(self):
            return _Rows()

    session = AsyncMock()
    session.execute = AsyncMock(return_value=_Result())

    with patch("plotlot.api.evidence.get_session", new=AsyncMock(return_value=session)):
        resp = await client.get("/api/v1/evidence", params={"workspace_id": "ws_1"})

    assert resp.status_code == 200
    data = resp.json()
    assert data[0]["id"] == "ev_1"
    assert data[0]["claim_key"] == "x"


@pytest.mark.asyncio
async def test_get_evidence_404_when_missing(client):
    session = AsyncMock()
    session.get = AsyncMock(return_value=None)
    with patch("plotlot.api.evidence.get_session", new=AsyncMock(return_value=session)):
        resp = await client.get("/api/v1/evidence/ev_missing")
    assert resp.status_code == 404
