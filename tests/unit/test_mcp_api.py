"""Unit tests for MCP HTTP endpoints."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, patch

import pytest

from plotlot.harness.approvals import approval_request_id, approval_request_json
from plotlot.storage.models import ApprovalRequest


class FakeSession:
    def __init__(
        self,
        *,
        rows_by_id: dict[str, object] | None = None,
        raise_on_get: bool = False,
    ):
        self.rows_by_id = rows_by_id or {}
        self.raise_on_get = raise_on_get
        self.added: list[object] = []
        self.committed = False
        self.rolled_back = False

    async def get(self, model, key):  # noqa: ANN001
        if self.raise_on_get:
            raise RuntimeError("boom")
        return self.rows_by_id.get(key)

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


@pytest.mark.asyncio
async def test_mcp_tools_call_write_external_with_valid_approval_skips_pending_and_does_not_persist_request(
    client,
):
    tool_name = "gmail_send_draft"
    run_id = "run_mcp_send_1"
    args = {"draft_id": "draft_email_123"}
    approval_id = approval_request_id(tool_name=tool_name, run_id=run_id, args=args)
    approved_row = ApprovalRequest(
        id=approval_id,
        workspace_id="ws_test",
        status="approved",
        risk_class="write_external",
        action_name=tool_name,
        reason="ok",
        request_json=approval_request_json(tool_name=tool_name, args=args, run_id=run_id),
        response_json={},
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    validation_session = FakeSession(rows_by_id={approval_id: approved_row})
    persistence_session = FakeSession()

    with patch(
        "plotlot.api.mcp.get_session",
        new=AsyncMock(side_effect=[validation_session, persistence_session]),
    ):
        resp = await client.post(
            "/api/v1/mcp/tools/call",
            json={
                "name": tool_name,
                "arguments": args,
                "context": {
                    "workspace_id": "ws_test",
                    "actor_user_id": "anonymous",
                    "run_id": run_id,
                    "project_id": "prj_test",
                    "risk_budget_cents": 0,
                    "live_network_allowed": False,
                    "approved_approval_ids": [approval_id],
                },
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "unavailable"
    assert data["decision"]["allowed"] is True
    assert data["decision"]["approval_required"] is False

    approvals = [obj for obj in persistence_session.added if isinstance(obj, ApprovalRequest)]
    assert approvals == []


@pytest.mark.asyncio
async def test_mcp_tools_call_write_external_with_invalid_approval_fails_closed_and_persists_request(
    client,
):
    tool_name = "gmail_send_draft"
    run_id = "run_mcp_send_2"
    args = {"draft_id": "draft_email_123"}
    approval_id = approval_request_id(tool_name=tool_name, run_id=run_id, args=args)
    wrong_workspace_row = ApprovalRequest(
        id=approval_id,
        workspace_id="ws_other",
        status="approved",
        risk_class="write_external",
        action_name=tool_name,
        reason="ok",
        request_json=approval_request_json(tool_name=tool_name, args=args, run_id=run_id),
        response_json={},
        expires_at=datetime.now(timezone.utc) + timedelta(hours=1),
    )

    validation_session = FakeSession(rows_by_id={approval_id: wrong_workspace_row})
    persistence_session = FakeSession()

    with patch(
        "plotlot.api.mcp.get_session",
        new=AsyncMock(side_effect=[validation_session, persistence_session]),
    ):
        resp = await client.post(
            "/api/v1/mcp/tools/call",
            json={
                "name": tool_name,
                "arguments": args,
                "context": {
                    "workspace_id": "ws_test",
                    "actor_user_id": "anonymous",
                    "run_id": run_id,
                    "project_id": "prj_test",
                    "risk_budget_cents": 0,
                    "live_network_allowed": False,
                    "approved_approval_ids": [approval_id],
                },
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending_approval"

    approvals = [obj for obj in persistence_session.added if isinstance(obj, ApprovalRequest)]
    assert len(approvals) == 1
    assert approvals[0].id == approval_id


@pytest.mark.asyncio
async def test_mcp_tools_call_approval_validation_db_error_fails_closed_and_persists_request(client):
    tool_name = "gmail_send_draft"
    run_id = "run_mcp_send_3"
    args = {"draft_id": "draft_email_123"}
    approval_id = approval_request_id(tool_name=tool_name, run_id=run_id, args=args)

    validation_session = FakeSession(raise_on_get=True)
    persistence_session = FakeSession()

    with patch(
        "plotlot.api.mcp.get_session",
        new=AsyncMock(side_effect=[validation_session, persistence_session]),
    ):
        resp = await client.post(
            "/api/v1/mcp/tools/call",
            json={
                "name": tool_name,
                "arguments": args,
                "context": {
                    "workspace_id": "ws_test",
                    "actor_user_id": "anonymous",
                    "run_id": run_id,
                    "project_id": "prj_test",
                    "risk_budget_cents": 0,
                    "live_network_allowed": False,
                    "approved_approval_ids": [approval_id],
                },
            },
        )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "pending_approval"

    approvals = [obj for obj in persistence_session.added if isinstance(obj, ApprovalRequest)]
    assert len(approvals) == 1
    assert approvals[0].id == approval_id


@pytest.mark.asyncio
async def test_mcp_tools_call_unknown_tool_returns_unknown_tool_status(client):
    resp = await client.post(
        "/api/v1/mcp/tools/call",
        json={
            "name": "totally_unknown_tool",
            "arguments": {},
            "context": {
                "workspace_id": "ws_test",
                "actor_user_id": "anonymous",
                "run_id": "run_mcp_unknown_1",
                "project_id": "prj_test",
                "risk_budget_cents": 0,
                "live_network_allowed": False,
                "approved_approval_ids": [],
            },
        },
    )

    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "unknown_tool"
