"""HTTP surface for MCP-like tool semantics.

This is not the full MCP protocol implementation. It exposes the two core
operations (tools/list and tools/call) over HTTP so clients can integrate while
the full MCP transport layer is stabilized.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import logging

from fastapi import APIRouter
from pydantic import BaseModel, Field

from plotlot.harness.default_runtime import get_default_runtime
from plotlot.harness.mcp_adapter import MCPAdapter
from plotlot.harness.approvals import approval_request_id, approval_request_json, is_valid_approved_approval
from plotlot.harness.tool_registry import tool_risk_class
from plotlot.land_use.models import ToolContext
from plotlot.storage.db import get_session
from plotlot.storage.models import ApprovalRequest


logger = logging.getLogger(__name__)


router = APIRouter(prefix="/api/v1/mcp", tags=["mcp"])


class MCPCallRequest(BaseModel):
    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)
    context: ToolContext
    approval_id: str | None = None


def _effective_approval_id(*, tool_name: str, args: dict[str, Any], context: ToolContext, provided: str | None) -> str:
    return provided or approval_request_id(tool_name=tool_name, run_id=context.run_id, args=args)


@router.get("/tools/list")
async def tools_list() -> list[dict[str, Any]]:
    adapter = MCPAdapter(get_default_runtime())
    return adapter.list_tools()


@router.post("/tools/call")
async def tools_call(body: MCPCallRequest) -> dict[str, Any]:
    adapter = MCPAdapter(get_default_runtime())

    claimed = set(body.context.approved_approval_ids or set())
    approval_id = _effective_approval_id(
        tool_name=body.name,
        args=body.arguments,
        context=body.context,
        provided=body.approval_id,
    )
    risk_class = tool_risk_class(body.name)
    validated: set[str] = set()
    if risk_class in {"write_external", "execution", "write_internal", "expensive_read"}:
        if approval_id in claimed:
            validation_session = await get_session()
            try:
                ok = await is_valid_approved_approval(
                    approval_id=approval_id,
                    workspace_id=body.context.workspace_id,
                    tool_name=body.name,
                    args=body.arguments,
                    run_id=body.context.run_id,
                    session=validation_session,
                )
                if ok:
                    validated = {approval_id}
            finally:
                await validation_session.close()
        body = body.model_copy(
            update={
                "context": body.context.model_copy(update={"approved_approval_ids": validated})
            }
        )

    result = await adapter.call_tool(
        name=body.name,
        arguments=body.arguments,
        context=body.context,
        approval_id=approval_id,
    )

    if result.status == "pending_approval" and result.decision.approval_id:
        session = await get_session()
        try:
            existing = await session.get(ApprovalRequest, result.decision.approval_id)
            desired_request = approval_request_json(
                tool_name=body.name,
                args=body.arguments,
                run_id=body.context.run_id,
            )
            if existing is None:
                session.add(
                    ApprovalRequest(
                        id=result.decision.approval_id,
                        workspace_id=body.context.workspace_id,
                        project_id=body.context.project_id,
                        analysis_run_id=body.context.analysis_run_id,
                        tool_run_id=body.context.tool_run_id,
                        status="pending",
                        risk_class=risk_class,
                        action_name=body.name,
                        reason=result.decision.reason,
                        request_json=desired_request,
                        response_json={},
                        requested_by=body.context.actor_user_id,
                    )
                )
                await session.commit()
            else:
                now = datetime.now(timezone.utc)
                expired = existing.expires_at is not None and existing.expires_at <= now
                if existing.status != "pending" or expired or existing.request_json != desired_request:
                    setattr(existing, "status", "pending")
                    setattr(existing, "reason", result.decision.reason)
                    setattr(existing, "request_json", desired_request)
                    setattr(existing, "response_json", {})
                    setattr(existing, "requested_by", body.context.actor_user_id)
                    setattr(existing, "decided_by", None)
                    setattr(existing, "decided_at", None)
                    if expired:
                        setattr(existing, "expires_at", None)
                    await session.commit()
        except Exception:
            logger.warning("Failed to persist approval request from MCP call", exc_info=True)
            try:
                await session.rollback()
            except Exception:
                logger.warning("Rollback failed", exc_info=True)
        finally:
            await session.close()
    return {
        "tool_name": result.tool_name,
        "status": result.status,
        "decision": result.decision.model_dump(),
        "result": result.result,
        "message": result.message,
    }
