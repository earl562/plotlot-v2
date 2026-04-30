"""Unit tests for MCP HTTP endpoints."""

from __future__ import annotations

from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_mcp_tools_list_includes_core_tools(client):
    resp = await client.get("/api/v1/mcp/tools/list")
    assert resp.status_code == 200
    data = resp.json()
    names = {t["name"] for t in data}
    assert "geocode_address" in names


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
