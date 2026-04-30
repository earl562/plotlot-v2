"""Typed events emitted by the harness runtime.

Transport adapters (REST/chat/MCP/frontend) should render these events as a
timeline with approvals, tool calls, evidence, and artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


EventKind = Literal[
    "run_started",
    "tool_call",
    "tool_result",
    "approval_required",
    "evidence_recorded",
    "run_completed",
]


@dataclass(frozen=True)
class HarnessEvent:
    kind: EventKind
    id: str
    payload: dict[str, Any]
