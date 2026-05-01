"""Approval helpers shared across transport adapters.

These utilities enforce a key invariant:

- An approved token must match the *exact* tool + run + args payload being executed.

Adapters (REST, chat, MCP) should use these helpers to:

- compute an approval_id that is stable for a given tool/run/args
- validate that an approval row is approved, unexpired, workspace-scoped, and bound to the payload

Fail-closed on any database error.
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone
from typing import Any

from plotlot.storage.db import get_session
from plotlot.storage.models import ApprovalRequest


logger = logging.getLogger(__name__)


def approval_request_json(*, tool_name: str, args: dict[str, Any], run_id: str) -> dict[str, Any]:
    return {"tool": tool_name, "args": args, "run_id": run_id}


def approval_request_id(*, tool_name: str, run_id: str, args: dict[str, Any]) -> str:
    """Generate a deterministic approval ID bound to the tool/run/args payload."""

    safe_tool = tool_name.replace(".", "_")
    payload = json.dumps(args, sort_keys=True, separators=(",", ":"), default=str)
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:10]
    return f"apr_{run_id}_{safe_tool}_{digest}"


async def is_valid_approved_approval(
    *,
    approval_id: str,
    workspace_id: str,
    tool_name: str,
    args: dict[str, Any],
    run_id: str,
    session: Any | None = None,
) -> bool:
    """Return True iff DB row is approved + unexpired + workspace-scoped + payload-bound."""

    close_after = False
    if session is None:
        session = await get_session()
        close_after = True
    try:
        row = await session.get(ApprovalRequest, approval_id)
        if row is None:
            return False

        if getattr(row, "workspace_id", None) != workspace_id:
            return False

        now = datetime.now(timezone.utc)
        if getattr(row, "status", None) != "approved":
            return False
        expires_at = getattr(row, "expires_at", None)
        if expires_at is not None and expires_at <= now:
            return False

        if getattr(row, "action_name", None) != tool_name:
            return False

        expected = approval_request_json(tool_name=tool_name, args=args, run_id=run_id)
        return getattr(row, "request_json", None) == expected
    except Exception:
        logger.warning("Approval validation failed; failing closed", exc_info=True)
        return False
    finally:
        if close_after:
            await session.close()
