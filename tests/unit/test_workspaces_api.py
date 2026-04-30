"""Unit tests for the workspace/project/site API.

These tests mock the DB session to validate endpoint wiring and contracts.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_list_workspaces_returns_rows(client):
    from plotlot.storage.models import Workspace

    class _Rows:
        def all(self):
            w = Workspace(id="ws_1", name="Acme", slug="acme")
            return [w]

    class _Result:
        def scalars(self):
            return _Rows()

    session = AsyncMock()
    session.execute = AsyncMock(return_value=_Result())

    with patch("plotlot.api.workspaces.get_session", new=AsyncMock(return_value=session)):
        resp = await client.get("/api/v1/workspaces")

    assert resp.status_code == 200
    assert resp.json() == [{"id": "ws_1", "name": "Acme", "slug": "acme"}]


@pytest.mark.asyncio
async def test_create_workspace_persists_and_returns_id(client):
    session = AsyncMock()
    session.add = MagicMock()

    with patch("plotlot.api.workspaces.get_session", new=AsyncMock(return_value=session)):
        resp = await client.post("/api/v1/workspaces", json={"name": "Acme"})

    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Acme"
    assert "id" in data
    session.add.assert_called_once()
    session.commit.assert_awaited_once()
