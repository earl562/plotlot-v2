"""Approval API for governed tool actions.

This is the minimal persistence surface to support:
- tool calls that emit pending approvals
- a user (or UI) approving/rejecting them
"""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from plotlot.storage.db import get_session
from plotlot.storage.models import ApprovalRequest


router = APIRouter(prefix="/api/v1", tags=["approvals"])


class ApprovalDecisionRequest(BaseModel):
    decision: str = Field(..., pattern="^(approve|reject)$")
    decided_by: str | None = None
    response_json: dict = Field(default_factory=dict)


@router.post("/approvals/{approval_id}/decision")
async def decide_approval(approval_id: str, body: ApprovalDecisionRequest):
    session = await get_session()
    try:
        approval = await session.get(ApprovalRequest, approval_id)
        if approval is None:
            raise HTTPException(status_code=404, detail="Approval not found")

        approval.status = "approved" if body.decision == "approve" else "rejected"
        approval.decided_by = body.decided_by
        approval.decided_at = datetime.now(timezone.utc)
        approval.response_json = body.response_json or {}
        await session.commit()
        return {
            "status": approval.status,
            "approval_id": approval.id,
        }
    finally:
        await session.close()


@router.get("/approvals/{approval_id}")
async def get_approval(approval_id: str):
    session = await get_session()
    try:
        approval = await session.get(ApprovalRequest, approval_id)
        if approval is None:
            raise HTTPException(status_code=404, detail="Approval not found")
        return {
            "approval_id": approval.id,
            "status": approval.status,
            "risk_class": approval.risk_class,
            "action_name": approval.action_name,
            "reason": approval.reason,
            "request_json": approval.request_json,
            "response_json": approval.response_json,
        }
    finally:
        await session.close()
