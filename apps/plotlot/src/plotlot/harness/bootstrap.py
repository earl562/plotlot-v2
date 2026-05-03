"""Default harness composition."""

from plotlot.harness.runtime import HarnessRuntime
from plotlot.harness.skill_registry import SkillRegistry
from plotlot.skills.zoning_research import ZoningResearchSkill


def build_default_runtime() -> HarnessRuntime:
    registry = SkillRegistry()
    registry.register(ZoningResearchSkill())
    return HarnessRuntime(registry=registry)
