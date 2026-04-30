"""Policy seam for harness tool execution."""

from __future__ import annotations

from plotlot.land_use.models import PolicyDecision, ToolContext
from plotlot.land_use.policy import ToolPolicy

from plotlot.harness.tool_registry import get_tool_contract


class HarnessPolicyEngine:
    """Authorize tool calls using ToolPolicy + tool contracts."""

    def __init__(self, policy: ToolPolicy | None = None) -> None:
        self._policy = policy or ToolPolicy()

    def authorize(
        self,
        *,
        tool_name: str,
        context: ToolContext,
        approval_id: str | None = None,
    ) -> PolicyDecision:
        contract = get_tool_contract(tool_name)
        return self._policy.authorize(contract, context, approval_id=approval_id)
