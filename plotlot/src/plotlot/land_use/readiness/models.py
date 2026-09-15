"""Bounded contracts for a site, its requirements, and supplied source records."""
from __future__ import annotations

import math
from datetime import date
from typing import Annotated, Literal

from pydantic import (
    BaseModel, ConfigDict, Field, HttpUrl, StrictBool, StrictFloat, StrictInt,
    StrictStr, StringConstraints, field_validator, model_validator,
)

Identifier = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
Value = StrictBool | StrictInt | StrictFloat | StrictStr
Category = Literal[
    "site_identity", "zoning", "access", "flood", "wetlands", "environmental",
    "geotechnical", "utilities", "schedule", "other",
]
FindingStatus = Literal[
    "supported", "missing_evidence", "potential_constraint", "confirmed_conflict",
    "contradiction", "dependency_blocked",
]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Requirement(Contract):
    id: Identifier
    category: Category
    label: str = Field(min_length=1, max_length=300)
    expected: Value
    comparison: Literal["eq", "gte", "lte"] = "eq"
    unit: str | None = Field(default=None, min_length=1, max_length=40)
    critical: StrictBool = True
    max_age_days: int = Field(default=180, ge=1, le=3650, strict=True)
    depends_on: list[Identifier] = Field(default_factory=list, max_length=80)
    due_on: date | None = None

    @field_validator("expected")
    @classmethod
    def finite_value(cls, value: Value) -> Value:
        if type(value) in (int, float) and abs(value) > 10**15:
            raise ValueError("Numeric magnitude must not exceed 1e15")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("Numbers must be finite")
        if isinstance(value, str) and (not value.strip() or len(value) > 1000):
            raise ValueError("Text values must contain 1 to 1000 characters")
        return value

    @model_validator(mode="after")
    def comparable(self) -> Requirement:
        numeric = type(self.expected) in (int, float)
        if self.comparison != "eq" and not numeric:
            raise ValueError("Ordered comparisons require a numeric expectation")
        if numeric and not self.unit:
            raise ValueError("Numeric expectations require an explicit unit")
        if len(set(self.depends_on)) != len(self.depends_on):
            raise ValueError("Duplicate requirement dependencies")
        return self


class Evidence(Contract):
    id: Identifier
    requirement_id: Identifier
    site_id: Identifier
    parcel_id: Identifier
    scenario_id: Identifier
    intended_use: str | None = Field(default=None, min_length=1, max_length=500)
    value: Value | None = None
    unit: str | None = Field(default=None, min_length=1, max_length=40)
    source_kind: Literal[
        "official_record", "professional_report", "utility_correspondence",
        "broker_material", "user_note",
    ]
    source_title: str = Field(min_length=1, max_length=500)
    source_url: HttpUrl | None = None
    document_id: Identifier | None = None
    locator: str = Field(default="", max_length=500)
    excerpt: str = Field(default="", max_length=4000)
    observed_on: date | None = None
    source_status: Literal["available", "unavailable", "not_found"] = "available"
    review_state: Literal["unreviewed", "source_checked"] = "unreviewed"
    screening_only: StrictBool = True
    active: StrictBool = True

    @field_validator("value")
    @classmethod
    def finite_value(cls, value: Value | None) -> Value | None:
        if value is None:
            return None
        return Requirement.finite_value(value)


class ReadinessCase(Contract):
    site_id: Identifier
    parcel_id: Identifier
    scenario_id: Identifier = "base"
    intended_use: str = Field(min_length=1, max_length=500)
    requirements: list[Requirement] = Field(min_length=1, max_length=80)
    evidence: list[Evidence] = Field(default_factory=list, max_length=400)

    @model_validator(mode="after")
    def valid_references(self) -> ReadinessCase:
        if not any(r.critical for r in self.requirements):
            raise ValueError("At least one critical requirement is required")
        by_id = {r.id: r for r in self.requirements}
        if len(by_id) != len(self.requirements):
            raise ValueError("Duplicate requirement IDs")
        if len({e.id for e in self.evidence}) != len(self.evidence):
            raise ValueError("Duplicate evidence IDs")
        if any(e.requirement_id not in by_id for e in self.evidence):
            raise ValueError("Evidence references an unknown requirement")
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(key: str) -> None:
            if key not in by_id:
                raise ValueError("Unknown requirement dependency")
            if key in visiting:
                raise ValueError("Requirement dependency cycle")
            if key in visited:
                return
            visiting.add(key)
            for dependency in by_id[key].depends_on:
                visit(dependency)
            visiting.remove(key)
            visited.add(key)

        for key in by_id:
            visit(key)
        return self


class Finding(Contract):
    requirement_id: str
    label: str
    category: Category
    critical: bool
    status: FindingStatus
    evidence_ids: list[str]
    issues: list[str]
    explanation: str


class NextAction(Contract):
    id: str
    requirement_id: str
    title: str
    suggested_owner: str
    priority: Literal["critical", "normal"]
    status: Literal["ready", "blocked"]
    depends_on: list[str]
    close_condition: str
    evidence_ids: list[str]
    due_on: date | None = None


class ReadinessReport(Contract):
    engine_version: str = "1.0.0"
    site_id: str
    parcel_id: str
    scenario_id: str
    intended_use: str
    evaluated_on: date
    fingerprint: str
    scope: Literal["supplied_requirements_only"] = "supplied_requirements_only"
    review_basis: Literal["user_supplied_source_checks"] = "user_supplied_source_checks"
    decision: Literal["hold", "do_not_proceed", "ready_for_review"]
    findings: list[Finding]
    actions: list[NextAction]
    supported_count: int
    unresolved_count: int
    critical_unresolved_count: int
    evidence: list[Evidence]
    disclaimer: str = (
        "DRAFT screening of supplied requirements and user-supplied source checks only. "
        "PlotLot has not independently verified the documents. Ready for review is not "
        "approval, certification, legal advice, or confirmation that a site is buildable. "
        "Obtain the applicable professional and authority determinations before relying "
        "on a development or acquisition decision."
    )


class ReportChange(Contract):
    field: str
    requirement_id: str | None = None
    before: str | None
    after: str | None


class SavedCase(Contract):
    revision: int
    case: ReadinessCase
    report: ReadinessReport
    changes: list[ReportChange]
    updated_at: str
    updated_by: str
    run_id: str


class SaveRequest(Contract):
    case: ReadinessCase
    expected_revision: int = Field(ge=0, strict=True)
