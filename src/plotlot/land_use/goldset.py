"""Loader and lightweight evaluator for agentic land-use gold-set cases."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal
import json

from pydantic import BaseModel, Field, model_validator

Operator = Literal["equals", "gte", "lte", "contains"]


class ExpectedClaim(BaseModel):
    """Expected claim/assertion for a gold-set case."""

    claim_key: str = Field(min_length=1)
    operator: Operator
    value: Any

    def evaluate(self, observed_claims: dict[str, Any]) -> bool:
        actual = observed_claims.get(self.claim_key)
        if self.operator == "equals":
            return bool(actual == self.value)
        if self.operator == "gte":
            return bool(actual is not None and actual >= self.value)
        if self.operator == "lte":
            return bool(actual is not None and actual <= self.value)
        if self.operator == "contains":
            return bool(actual is not None and self.value in actual)
        raise AssertionError(f"unsupported operator: {self.operator}")


class GoldCase(BaseModel):
    """A deterministic task fixture for evaluating the land-use harness."""

    id: str = Field(min_length=1)
    persona: str = Field(min_length=1)
    workflow: str = Field(min_length=1)
    fixture_mode: str = Field(min_length=1)
    task: str = Field(min_length=1)
    required_tools: list[str] = Field(min_length=1)
    expected_claims: list[ExpectedClaim] = Field(min_length=1)
    forbidden: list[str] = Field(default_factory=list)
    site: dict[str, Any] | None = None
    site_group: list[dict[str, Any]] | None = None
    external_source_text: str | None = None

    @model_validator(mode="after")
    def _require_site_or_group(self) -> "GoldCase":
        if not self.site and not self.site_group:
            raise ValueError("gold cases require site or site_group")
        if self.site_group is not None and len(self.site_group) < 2:
            raise ValueError("site_group cases require at least two candidate sites")
        return self


class GoldSet(BaseModel):
    """Collection of land-use harness gold cases."""

    schema_version: str = Field(min_length=1)
    created_at: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    global_invariants: list[str] = Field(min_length=1)
    cases: list[GoldCase] = Field(min_length=1)

    @model_validator(mode="after")
    def _case_ids_must_be_unique(self) -> "GoldSet":
        ids = [case.id for case in self.cases]
        duplicates = {case_id for case_id in ids if ids.count(case_id) > 1}
        if duplicates:
            raise ValueError(f"duplicate gold case IDs: {sorted(duplicates)}")
        return self

    def by_id(self, case_id: str) -> GoldCase:
        for case in self.cases:
            if case.id == case_id:
                return case
        raise KeyError(case_id)

    def required_tools(self) -> set[str]:
        tools: set[str] = set()
        for case in self.cases:
            tools.update(case.required_tools)
        return tools


def default_goldset_path() -> Path:
    """Return the repo-local land-use gold-set path."""

    return Path(__file__).resolve().parents[3] / "tests" / "golden" / "land_use_cases.json"


def load_land_use_goldset(path: str | Path | None = None) -> GoldSet:
    """Load and validate the land-use gold-set JSON file."""

    resolved = Path(path) if path is not None else default_goldset_path()
    with resolved.open() as f:
        return GoldSet.model_validate(json.load(f))
