"""Thin MCP-style adapter over internal PlotLot tools.

This keeps MCP as an external adapter. The internal product contract remains
the FastAPI/harness/tool layer.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from plotlot.api.ordinances import ExtractRulesRequest, extract_rules, search_ordinance_records
from plotlot.storage.db import get_session

router = APIRouter(prefix="/api/v1/mcp", tags=["mcp"])


class MCPInvokeRequest(BaseModel):
    name: str
    input: dict[str, Any] = Field(default_factory=dict)


MCP_TOOLS: list[dict[str, Any]] = [
    {
        "name": "plotlot.search_ordinance",
        "description": "Search PlotLot's ordinance intelligence index for cited zoning sections.",
        "input_schema": {
            "type": "object",
            "properties": {
                "municipality": {"type": "string"},
                "query": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50},
            },
            "required": ["municipality", "query"],
        },
    },
    {
        "name": "plotlot.get_zoning_rules",
        "description": "Return candidate normalized zoning rules for a zoning code.",
        "input_schema": {
            "type": "object",
            "properties": {
                "municipality": {"type": "string"},
                "zoning_code": {"type": "string"},
            },
            "required": ["municipality", "zoning_code"],
        },
    },
]


@router.post("/tools/list")
async def list_tools() -> dict[str, Any]:
    return {"tools": MCP_TOOLS}


@router.post("/tools/invoke")
async def invoke_tool(
    payload: MCPInvokeRequest,
    session: AsyncSession = Depends(get_session),
) -> dict[str, Any]:
    if payload.name == "plotlot.search_ordinance":
        municipality = payload.input.get("municipality")
        query = payload.input.get("query")
        if not municipality or not query:
            raise HTTPException(status_code=422, detail="municipality and query are required")
        hits = await search_ordinance_records(
            session,
            municipality=municipality,
            query=query,
            limit=int(payload.input.get("limit", 10)),
        )
        return {
            "status": "success",
            "tool": payload.name,
            "result": {"results": [hit.model_dump() for hit in hits]},
        }

    if payload.name == "plotlot.get_zoning_rules":
        municipality = payload.input.get("municipality")
        zoning_code = payload.input.get("zoning_code")
        if not municipality or not zoning_code:
            raise HTTPException(status_code=422, detail="municipality and zoning_code are required")
        result = await extract_rules(
            ExtractRulesRequest(municipality=municipality, zoning_code=zoning_code),
            session,
        )
        return {"status": "success", "tool": payload.name, "result": result.model_dump()}

    raise HTTPException(status_code=404, detail=f"Unsupported MCP tool: {payload.name}")
