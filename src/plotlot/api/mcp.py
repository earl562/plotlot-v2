"""HTTP surface for MCP-like tool semantics.

This is not the full MCP protocol implementation. It exposes the two core
operations (tools/list and tools/call) over HTTP so clients can integrate while
the full MCP transport layer is stabilized.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from plotlot.harness.default_runtime import get_default_runtime
from plotlot.harness.mcp_adapter import MCPAdapter
from plotlot.land_use.models import ToolContext


router = APIRouter(prefix="/api/v1/mcp", tags=["mcp"])


class MCPCallRequest(BaseModel):
    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)
    context: ToolContext
    approval_id: str | None = None


@router.get("/tools/list")
async def tools_list() -> list[dict[str, Any]]:
    adapter = MCPAdapter(get_default_runtime())
    return adapter.list_tools()


@router.post("/tools/call")
async def tools_call(body: MCPCallRequest) -> dict[str, Any]:
    adapter = MCPAdapter(get_default_runtime())
    result = await adapter.call_tool(
        name=body.name,
        arguments=body.arguments,
        context=body.context,
        approval_id=body.approval_id,
    )
    return {
        "tool_name": result.tool_name,
        "status": result.status,
        "decision": result.decision.model_dump(),
        "result": result.result,
        "message": result.message,
    }
