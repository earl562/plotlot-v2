"""Minimal harness runtime for skill execution."""

from __future__ import annotations

from plotlot.harness.context_broker import ContextBroker
from plotlot.harness.contracts import SkillInput, SkillOutput
from plotlot.harness.skill_registry import SkillRegistry


class HarnessRuntime:
    """Routes prompts to registered skills and executes them."""

    def __init__(
        self,
        *,
        registry: SkillRegistry | None = None,
        context_broker: ContextBroker | None = None,
    ) -> None:
        self.registry = registry or SkillRegistry()
        self.context_broker = context_broker or ContextBroker()

    async def run(self, skill_input: SkillInput, skill_name: str | None = None) -> SkillOutput:
        skill = (
            self.registry.get(skill_name) if skill_name else self.registry.route(skill_input.prompt)
        )
        if skill is None:
            return SkillOutput(
                status="no_skill",
                summary="No matching skill was registered for this request.",
                open_questions=["Choose a skill or provide a more specific land-use task."],
            )
        return await skill.run(skill_input)
