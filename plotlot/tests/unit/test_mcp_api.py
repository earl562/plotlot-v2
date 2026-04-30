"""Unit tests for MCP HTTP endpoints."""

from __future__ import annotations

from unittest.mock import patch

import pytest


class FakeSession:
    def __init__(self):
        self.added = []
        self.committed = False
        self.rolled_back = False

    async def get(self, model, key):  # noqa: ANN001
        return None

    def add(self, obj):  # noqa: ANN001
        self.added.append(obj)

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    async def close(self):
        return None


@pytest.mark.asyncio
async def test_mcp_tools_list_includes_core_tools(client):
    resp = await client.get("/api/v1/mcp/tools/list")
    assert resp.status_code == 200
    data = resp.json()
    names = {t["name"] for t in data}
    assert "geocode_address" in names
    assert "draft_email" in names


@pytest.mark.asyncio
async def test_mcp_tools_call_geocode(client):
    async def _fake_geocode(address: str):
        return {
            "formatted_address": address,
            "municipality": "Example",
            "county": "Example",
            "state": "FL",
            "lat": 1.23,
            "lng": 4.56,
        }

    with patch("plotlot.retrieval.geocode.geocode_address", new=_fake_geocode):
        resp = await client.post(
            "/api/v1/mcp/tools/call",
            json={
                "name": "geocode_address",
                "arguments": {"address": "123 Main St"},
                "context": {
                    "workspace_id": "ws_test",
                    "actor_user_id": "anonymous",
                    "run_id": "run_mcp_1",
                    "project_id": "prj_test",
                    "risk_budget_cents": 0,
                    "live_network_allowed": False,
                    "approved_approval_ids": [],
                },
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["result"]["status"] == "success"
    assert data["result"]["result"]["municipality"] == "Example"


@pytest.mark.asyncio
async def test_mcp_tools_call_write_external_requires_approval_and_persists_request(client):
    from unittest.mock import AsyncMock

    from plotlot.storage.models import ApprovalRequest

    fake_session = FakeSession()

    with patch("plotlot.api.mcp.get_session", new=AsyncMock(return_value=fake_session)):
        resp = await client.post(
            "/api/v1/mcp/tools/call",
            json={
                "name": "gmail_send_draft",
                "arguments": {"draft_id": "draft_email_123"},
                "context": {
                    "workspace_id": "ws_test",
                    "actor_user_id": "anonymous",
                    "run_id": "run_mcp_send_1",
                    "project_id": "prj_test",
                    "risk_budget_cents": 0,
                    "live_network_allowed": False,
                    "approved_approval_ids": [],
                },
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending_approval"
    assert data["decision"]["approval_required"] is True
    assert data["decision"]["approval_id"]

    approvals = [obj for obj in fake_session.added if isinstance(obj, ApprovalRequest)]
    assert len(approvals) == 1
    assert approvals[0].action_name == "gmail_send_draft"
