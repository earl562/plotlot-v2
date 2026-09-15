"""Deterministic screening. Evidence is data, never an instruction or approval."""
from __future__ import annotations

import hashlib
import json
from datetime import date

from .models import (
    Evidence, Finding, NextAction, ReadinessCase, ReadinessReport, ReportChange, Requirement,
)

OWNERS = {
    "site_identity": "Acquisition manager / surveyor",
    "zoning": "Land-use planner / local authority",
    "access": "Surveyor / title counsel",
    "flood": "Civil engineer / floodplain authority",
    "wetlands": "Qualified environmental consultant",
    "environmental": "Qualified environmental professional",
    "geotechnical": "Geotechnical engineer",
    "utilities": "Utility representative / infrastructure engineer",
    "schedule": "Development manager",
    "other": "Assigned diligence reviewer",
}


def _issues(e: Evidence, r: Requirement, case: ReadinessCase, today: date) -> list[str]:
    issues = []
    for field in ("site_id", "parcel_id", "scenario_id"):
        if getattr(e, field) != getattr(case, field):
            issues.append(field.replace("_id", "") + "_mismatch")
    if e.intended_use is None:
        issues.append("missing_use_scope")
    elif e.intended_use.casefold() != case.intended_use.casefold():
        issues.append("intended_use_mismatch")
    if e.source_status != "available":
        issues.append("source_unavailable")
    if not (e.source_url or e.document_id):
        issues.append("missing_source")
    if not (e.locator and e.excerpt):
        issues.append("missing_locator")
    if e.observed_on is None:
        issues.append("missing_date")
    elif e.observed_on > today:
        issues.append("future_dated")
    elif (today - e.observed_on).days > r.max_age_days:
        issues.append("stale")
    if e.value is None:
        issues.append("unknown_value")
    elif type(r.expected) in (int, float):
        if type(e.value) not in (int, float):
            issues.append("value_type_mismatch")
    elif type(e.value) is not type(r.expected):
        issues.append("value_type_mismatch")
    if (e.unit or "").casefold() != (r.unit or "").casefold():
        issues.append("unit_mismatch")
    return issues


def _normalized(value: object) -> tuple[str, object]:
    if type(value) in (int, float):
        return "number", float(value)  # type: ignore[arg-type]
    if isinstance(value, str):
        return "text", value.casefold()
    return "boolean", value


def _supports(e: Evidence, r: Requirement) -> bool:
    if r.comparison == "eq":
        return _normalized(e.value) == _normalized(r.expected)
    # Types and units have already been checked; no unit conversion is inferred.
    actual, expected = float(e.value), float(r.expected)  # type: ignore[arg-type]
    return actual >= expected if r.comparison == "gte" else actual <= expected


def _finding(r: Requirement, case: ReadinessCase, today: date) -> Finding:
    records = sorted(
        (e for e in case.evidence if e.requirement_id == r.id and e.active), key=lambda e: e.id
    )
    admissible = []
    issues: set[str] = set()
    for record in records:
        invalid = _issues(record, r, case, today)
        issues.update(invalid)
        if not invalid:
            admissible.append(record)
    status = "missing_evidence"
    explanation = "Obtain applicable, current, source-linked evidence for this requirement."
    if len({_normalized(e.value) for e in admissible}) > 1:
        status = "contradiction"
        issues.add("conflicting_active_records")
        explanation = "Active applicable source records disagree. Resolve them explicitly."
    elif admissible and issues:
        status = "potential_constraint"
        explanation = "Some active records are inapplicable or incomplete; resolve them before relying."
    elif admissible:
        reviewed = [
            e for e in admissible
            if e.review_state == "source_checked" and not e.screening_only
            and e.source_kind not in ("broker_material", "user_note")
        ]
        if not reviewed:
            status = "potential_constraint"
            issues.add("review_or_site_specific_confirmation_required")
            explanation = "Screening or unreviewed material cannot establish a site-specific conclusion."
        elif _supports(reviewed[0], r):
            status = "supported"
            explanation = "The supplied source-checked record supports this requirement; reviewer acceptance remains required."
        else:
            status = "confirmed_conflict"
            explanation = "The supplied source-checked record conflicts with this scenario requirement."
    return Finding(
        requirement_id=r.id, label=r.label, category=r.category, critical=r.critical,
        status=status, evidence_ids=[e.id for e in records], issues=sorted(issues),
        explanation=explanation,
    )


def _ordered_requirements(case: ReadinessCase) -> list[Requirement]:
    remaining = {r.id: r for r in case.requirements}
    done: set[str] = set()
    ordered = []
    while remaining:
        available = [r for r in remaining.values() if set(r.depends_on) <= done]
        available.sort(key=lambda r: (not r.critical, r.due_on or date.max, r.id))
        # ReadinessCase validates the graph, so at least one node is always available.
        r = available[0]
        ordered.append(r)
        done.add(r.id)
        del remaining[r.id]
    return ordered


def evaluate(case: ReadinessCase, *, today: date | None = None) -> ReadinessReport:
    """Evaluate only supplied requirements; does not fetch, persist, or authorize."""
    today = today or date.today()
    findings: dict[str, Finding] = {}
    actions = []
    for requirement in _ordered_requirements(case):
        finding = _finding(requirement, case, today)
        blocked = [
            key for key in sorted(requirement.depends_on) if findings[key].status != "supported"
        ]
        if blocked and finding.status == "supported":
            finding = finding.model_copy(update={
                "status": "dependency_blocked", "issues": ["unresolved_prerequisite"],
                "explanation": "Resolve prerequisite requirements: " + ", ".join(blocked),
            })
        findings[requirement.id] = finding
        if finding.status != "supported":
            actions.append(NextAction(
                id="task:" + requirement.id, requirement_id=requirement.id,
                title=("Resolve conflicting records: " if finding.status == "contradiction"
                       else "Resolve: ") + requirement.label,
                suggested_owner=OWNERS[requirement.category],
                priority="critical" if requirement.critical else "normal",
                status="blocked" if blocked else "ready",
                depends_on=["task:" + key for key in blocked],
                close_condition=(
                    "Record applicable, current, source-checked evidence for this parcel and scenario; "
                    "resolve active contradictions and prerequisites, then rerun the requirement. "
                    "Changing a task label alone does not clear the finding."
                ),
                evidence_ids=finding.evidence_ids, due_on=requirement.due_on,
            ))
    ordered_findings = sorted(findings.values(), key=lambda f: f.requirement_id)
    critical_unresolved = [f for f in ordered_findings if f.critical and f.status != "supported"]
    decision = "ready_for_review"
    if any(f.status == "confirmed_conflict" for f in critical_unresolved):
        decision = "do_not_proceed"
    elif critical_unresolved:
        decision = "hold"
    canonical = case.model_dump(mode="json")
    canonical["requirements"] = sorted(canonical["requirements"], key=lambda r: r["id"])
    for requirement in canonical["requirements"]:
        requirement["depends_on"] = sorted(requirement["depends_on"])
    canonical["evidence"] = sorted(canonical["evidence"], key=lambda e: e["id"])
    fingerprint = hashlib.sha256(json.dumps(
        {"case": canonical, "evaluated_on": today.isoformat(), "engine_version": "1.0.0"},
        sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode()).hexdigest()
    supported = sum(f.status == "supported" for f in ordered_findings)
    return ReadinessReport(
        site_id=case.site_id, parcel_id=case.parcel_id, scenario_id=case.scenario_id,
        intended_use=case.intended_use, evaluated_on=today, fingerprint=fingerprint,
        decision=decision, findings=ordered_findings, actions=actions,
        supported_count=supported, unresolved_count=len(ordered_findings)-supported,
        critical_unresolved_count=len(critical_unresolved),
        evidence=sorted(case.evidence, key=lambda e: e.id),
    )


def diff_reports(before: ReadinessReport, after: ReadinessReport) -> list[ReportChange]:
    """Explain changes between saved memos without mutating either version."""
    if (before.site_id, before.parcel_id) != (after.site_id, after.parcel_id):
        raise ValueError("Reports must refer to the same site and parcel")
    changes = []
    for field in ("decision", "scenario_id", "intended_use"):
        old, new = getattr(before, field), getattr(after, field)
        if old != new:
            changes.append(ReportChange(field=field, before=old, after=new))
    old_findings = {f.requirement_id: f for f in before.findings}
    new_findings = {f.requirement_id: f for f in after.findings}
    for key in sorted(old_findings.keys() | new_findings.keys()):
        old, new = old_findings.get(key), new_findings.get(key)
        if old != new:
            changes.append(ReportChange(
                field="finding", requirement_id=key,
                before=old.status if old else None, after=new.status if new else None,
            ))
    old_evidence = {e.id: e.model_dump_json() for e in before.evidence}
    new_evidence = {e.id: e.model_dump_json() for e in after.evidence}
    for key in sorted(old_evidence.keys() | new_evidence.keys()):
        if old_evidence.get(key) != new_evidence.get(key):
            changes.append(ReportChange(
                field="evidence", before=key if key in old_evidence else None,
                after=key if key in new_evidence else None,
            ))
    return changes
