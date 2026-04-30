"""Unit tests for REST tool surfaces and MCP equivalence."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

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

    async def flush(self):
        return None

    async def commit(self):
        self.committed = True

    async def rollback(self):
        self.rolled_back = True

    async def close(self):
        return None


@pytest.mark.asyncio
async def test_list_tools_returns_contracts(client):
    resp = await client.get("/api/v1/tools")
    assert resp.status_code == 200
    data = resp.json()
    names = {t["name"] for t in data}
    assert "geocode_address" in names
    assert "search_municode_live" in names


@pytest.mark.asyncio
async def test_tools_call_geocode_matches_mcp_adapter(client):
    from plotlot.harness.default_runtime import get_default_runtime
    from plotlot.harness.mcp_adapter import MCPAdapter
    from plotlot.land_use.models import ToolContext

    fake_session = FakeSession()

    async def _fake_geocode(address: str):
        return {
            "formatted_address": address,
            "municipality": "Example",
            "county": "Example",
            "state": "FL",
            "lat": 1.23,
            "lng": 4.56,
        }

    with (
        patch("plotlot.api.tools.get_session", new=AsyncMock(return_value=fake_session)),
        patch("plotlot.retrieval.geocode.geocode_address", new=_fake_geocode),
    ):
        # REST
        run_id = "run_test_1"
        resp = await client.post(
            "/api/v1/tools/call",
            json={
                "tool_name": "geocode_address",
                "arguments": {"address": "123 Main St"},
                "workspace_id": "ws_test",
                "run_id": run_id,
            },
        )
        assert resp.status_code == 200
        rest = resp.json()
        assert rest["status"] == "ok"
        assert rest["result"]["status"] == "success"
        assert rest["result"]["result"]["municipality"] == "Example"

        # MCP
        runtime = get_default_runtime()
        adapter = MCPAdapter(runtime)
        mcp_result = await adapter.call_tool(
            name="geocode_address",
            arguments={"address": "123 Main St"},
            context=ToolContext(
                workspace_id="ws_test",
                actor_user_id="anonymous",
                run_id=run_id,
                project_id="prj_test",
                risk_budget_cents=0,
            ),
        )
        assert mcp_result.status == "ok"
        assert mcp_result.result is not None
        assert mcp_result.result["status"] == "success"
        assert mcp_result.result["result"]["municipality"] == "Example"


@pytest.mark.asyncio
async def test_tools_call_expensive_read_requires_approval(client):
    fake_session = FakeSession()
    with patch("plotlot.api.tools.get_session", new=AsyncMock(return_value=fake_session)):
        resp = await client.post(
            "/api/v1/tools/call",
            json={
                "tool_name": "search_municode_live",
                "arguments": {"municipality": "Example", "query": "parking"},
                "workspace_id": "ws_test",
                "risk_budget_cents": 0,
                "run_id": "run_test_2",
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending_approval"
    assert data["decision"]["approval_required"] is True
    assert data["decision"]["approval_id"]


@pytest.mark.asyncio
async def test_tools_call_search_zoning_ordinance_records_evidence_and_matches_mcp(client):
    from plotlot.core.types import SearchResult
    from plotlot.harness.default_runtime import get_default_runtime
    from plotlot.harness.mcp_adapter import MCPAdapter
    from plotlot.land_use.models import ToolContext

    fake_api_session = FakeSession()
    fake_search_session = FakeSession()

    async def _fake_hybrid_search(session, municipality: str, zone_code: str, limit: int = 10, embedding=None):
        assert municipality == "Example City"
        assert zone_code == "parking"
        return [
            SearchResult(
                section="33-123",
                section_title="Off-street parking",
                zone_codes=["R-1"],
                chunk_text="Two spaces per dwelling unit.",
                score=0.99,
                municipality=municipality,
            )
        ]

    async def _fake_get_session_for_search():
        return fake_search_session

    with (
        patch("plotlot.api.tools.get_session", new=AsyncMock(return_value=fake_api_session)),
        patch("plotlot.storage.db.get_session", new=_fake_get_session_for_search),
        patch("plotlot.retrieval.search.hybrid_search", new=_fake_hybrid_search),
    ):
        run_id = "run_test_4"
        resp = await client.post(
            "/api/v1/tools/call",
            json={
                "tool_name": "search_zoning_ordinance",
                "arguments": {"municipality": "Example City", "query": "parking"},
                "workspace_id": "ws_test",
                "run_id": run_id,
            },
        )
        assert resp.status_code == 200
        rest = resp.json()
        assert rest["status"] == "ok"
        assert rest["result"]["status"] == "success"
        assert rest["evidence_ids"]
        assert rest["result"]["results"][0]["evidence_id"] in set(rest["evidence_ids"])

        runtime = get_default_runtime()
        adapter = MCPAdapter(runtime)
        mcp_result = await adapter.call_tool(
            name="search_zoning_ordinance",
            arguments={"municipality": "Example City", "query": "parking"},
            context=ToolContext(
                workspace_id="ws_test",
                actor_user_id="anonymous",
                run_id=run_id,
                project_id="prj_test",
                risk_budget_cents=0,
            ),
        )
        assert mcp_result.status == "ok"
        assert mcp_result.result is not None
        assert mcp_result.result["status"] == "success"
        assert mcp_result.result["results"][0]["section"] == "33-123"


@pytest.mark.asyncio
async def test_tools_call_generate_document_persists_artifacts(client):
    fake_session = FakeSession()
    with patch("plotlot.api.tools.get_session", new=AsyncMock(return_value=fake_session)):
        resp = await client.post(
            "/api/v1/tools/call",
            json={
                "tool_name": "generate_document",
                "arguments": {
                    "title": "Test Report",
                    "evidence_ids": ["ev_1", "ev_2"],
                },
                "workspace_id": "ws_test",
                "run_id": "run_test_3",
            },
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "report_id" in data["artifact_ids"]
    assert "document_id" in data["artifact_ids"]
