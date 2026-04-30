"""Tests for transport-agnostic land-use tool contracts."""

import pytest
from pydantic import ValidationError

from plotlot.land_use import ToolContract, ToolRiskClass


def test_tool_contract_accepts_rest_chat_and_mcp_safe_names():
    contract = ToolContract(
        name="plotlot.search_ordinances",
        description="Search ordinance sections with citations.",
        risk_class=ToolRiskClass.READ_ONLY,
        input_schema={"type": "object"},
        output_schema={"type": "array"},
    )

    assert contract.name == "plotlot.search_ordinances"
    assert contract.risk_class == "read_only"
    assert contract.timeout_seconds == 30


def test_tool_contract_rejects_unsafe_names_and_negative_budget():
    with pytest.raises(ValidationError, match="tool names"):
        ToolContract(
            name="send email now!",
            description="Unsafe name",
            risk_class=ToolRiskClass.WRITE_EXTERNAL,
            input_schema={},
            output_schema={},
        )

    with pytest.raises(ValidationError):
        ToolContract(
            name="search_ordinances",
            description="Search",
            risk_class=ToolRiskClass.READ_ONLY,
            input_schema={},
            output_schema={},
            budget_cents=-1,
        )
