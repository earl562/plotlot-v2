"""Behavioral acceptance cases for evidence-backed feasibility screening."""
from datetime import date, timedelta
from importlib import import_module
from pathlib import Path

import pytest
from pydantic import ValidationError

TODAY = date(2026, 9, 14)


def modules():
    root = Path(__file__).resolve().parents[2] / "src/plotlot/land_use/readiness"
    assert (root / "engine.py").exists(), "Site-readiness engine has not been implemented"
    return import_module("plotlot.land_use.readiness.models"), import_module(
        "plotlot.land_use.readiness.engine"
    )


def requirement(**changes):
    return dict(id="access", category="access", label="Legal access established",
                expected=True, comparison="eq", critical=True, **changes)


def case_dict(requirements=None, evidence=None, **changes):
    return dict(site_id="s1", parcel_id="p1", scenario_id="base",
                intended_use="Residential development", requirements=requirements or [requirement()],
                evidence=evidence or [], **changes)


def record(**changes):
    value = dict(id="e1", requirement_id="access", site_id="s1", parcel_id="p1",
                 scenario_id="base", intended_use="Residential development", value=True, source_kind="professional_report",
                 source_title="Supplied survey", document_id="survey-1", locator="Page 2",
                 excerpt="The supplied access finding applies to parcel p1.",
                 observed_on=TODAY.isoformat(), review_state="source_checked", screening_only=False)
    value.update(changes)
    return value


def evaluate(data, today=TODAY):
    m, e = modules()
    return e.evaluate(m.ReadinessCase.model_validate(data), today=today)


def test_unknown_critical_evidence_holds_decision():
    result = evaluate(case_dict())
    assert result.decision == "hold"
    assert result.findings[0].status == "missing_evidence"
    assert result.actions[0].requirement_id == "access"
    assert result.actions[0].close_condition
    assert result.scope == "supplied_requirements_only"


def test_supported_is_ready_for_review_not_approved():
    result = evaluate(case_dict(evidence=[record()]))
    assert result.decision == "ready_for_review"
    assert result.findings[0].status == "supported"
    assert result.findings[0].evidence_ids == ["e1"]
    assert result.disclaimer
    assert result.review_basis == "user_supplied_source_checks"


def test_confirmed_critical_conflict_prevents_proceeding():
    result = evaluate(case_dict(evidence=[record(value=False)]))
    assert result.decision == "do_not_proceed"
    assert result.findings[0].status == "confirmed_conflict"


@pytest.mark.parametrize("overrides", [
    {"review_state": "unreviewed"}, {"screening_only": True},
    {"source_kind": "broker_material"}, {"source_kind": "user_note"},
])
def test_weak_evidence_never_clears_critical_requirement(overrides):
    result = evaluate(case_dict(evidence=[record(**overrides)]))
    assert result.decision == "hold"
    assert result.findings[0].status == "potential_constraint"


@pytest.mark.parametrize("overrides,reason", [
    ({"site_id": "other"}, "site_mismatch"),
    ({"parcel_id": "other"}, "parcel_mismatch"),
    ({"scenario_id": "other"}, "scenario_mismatch"),
    ({"observed_on": "2025-01-01"}, "stale"),
    ({"observed_on": "2026-09-15"}, "future_dated"),
    ({"observed_on": None}, "missing_date"),
    ({"document_id": None, "source_url": None}, "missing_source"),
    ({"locator": "", "excerpt": ""}, "missing_locator"),
    ({"value": None}, "unknown_value"),
    ({"source_status": "unavailable"}, "source_unavailable"),
])
def test_invalid_or_unavailable_evidence_cannot_create_a_pass(overrides, reason):
    result = evaluate(case_dict(evidence=[record(**overrides)]))
    assert result.decision == "hold"
    assert reason in result.findings[0].issues


def test_evidence_exactly_at_freshness_boundary_is_usable():
    req = requirement(max_age_days=30)
    result = evaluate(case_dict([req], [record(observed_on=(TODAY-timedelta(days=30)).isoformat())]))
    assert result.decision == "ready_for_review"


def test_active_contradiction_takes_precedence_over_favorable_record():
    result = evaluate(case_dict(evidence=[record(), record(id="e2", value=False)]))
    assert result.decision == "hold"
    assert result.findings[0].status == "contradiction"
    assert set(result.findings[0].evidence_ids) == {"e1", "e2"}


def test_inactive_superseded_record_is_not_a_live_contradiction():
    result = evaluate(case_dict(evidence=[record(), record(id="old", value=False, active=False)]))
    assert result.decision == "ready_for_review"


def test_unreviewed_contradictory_record_still_requires_resolution():
    result = evaluate(case_dict(evidence=[record(), record(id="e2", value=False, review_state="unreviewed")]))
    assert result.decision == "hold"
    assert result.findings[0].status == "contradiction"


def test_numeric_threshold_preserves_zero():
    req = dict(id="area", category="site_identity", label="Usable acres", expected=1.0,
               comparison="gte", unit="acre", critical=True)
    result = evaluate(case_dict([req], [record(requirement_id="area", value=0, unit="acre")]))
    assert result.findings[0].status == "confirmed_conflict"


@pytest.mark.parametrize("value,unit,issue", [(4, "sqft", "unit_mismatch"),
                                             (True, "acre", "value_type_mismatch"),
                                             ("10", "acre", "value_type_mismatch")])
def test_incomparable_units_and_types_do_not_clear(value, unit, issue):
    req = dict(id="area", category="site_identity", label="Usable acres", expected=1.0,
               comparison="gte", unit="acre", critical=True)
    result = evaluate(case_dict([req], [record(requirement_id="area", value=value, unit=unit)]))
    assert result.decision == "hold"
    assert issue in result.findings[0].issues


def test_false_boolean_expectation_is_not_missing():
    req = requirement()
    req["expected"] = False
    assert evaluate(case_dict([req], [record(value=False)])).decision == "ready_for_review"


def test_case_order_does_not_change_result_or_fingerprint():
    records = [record(id="b"), record(id="a")]
    a = evaluate(case_dict(evidence=records)).model_dump()
    b = evaluate(case_dict(evidence=list(reversed(records)))).model_dump()
    assert a == b


def test_optional_missing_does_not_hide_unresolved_action():
    optional = dict(id="fiber", category="utilities", label="Fiber confirmation",
                    expected=True, critical=False)
    result = evaluate(case_dict([requirement(), optional], [record()]))
    assert result.decision == "ready_for_review"
    assert result.unresolved_count == 1
    assert result.actions[0].requirement_id == "fiber"


def test_dependencies_remain_blocked_until_prerequisite_supported():
    dependent = dict(id="plan", category="zoning", label="Concept accepted", expected=True,
                     depends_on=["access"])
    result = evaluate(case_dict([requirement(), dependent], [record(requirement_id="plan")]))
    finding = next(f for f in result.findings if f.requirement_id == "plan")
    assert finding.status == "dependency_blocked"
    assert result.actions[0].requirement_id == "access"


@pytest.mark.parametrize("mutation", [
    lambda d: d.update(requirements=[]),
    lambda d: d["requirements"].append(d["requirements"][0].copy()),
    lambda d: d.update(evidence=[record(), record()]),
    lambda d: d.update(evidence=[record(requirement_id="missing")]),
    lambda d: d["requirements"][0].update(depends_on=["missing"]),
    lambda d: d["requirements"][0].update(depends_on=["access"]),
    lambda d: d.update(site_id="   "),
    lambda d: d.update(extra_untrusted_field="ignored?"),
    lambda d: d["requirements"][0].update(expected=float("nan")),
    lambda d: d["requirements"][0].update(expected=float("inf")),
    lambda d: d["requirements"][0].update(comparison="gte", expected=True),
    lambda d: d["requirements"][0].update(comparison="gte", expected=5, unit=None),
    lambda d: d.update(evidence=[record(source_url="javascript:alert(1)")]),
])
def test_invalid_input_rejected_instead_of_silently_coerced(mutation):
    m, _ = modules()
    data = case_dict()
    mutation(data)
    with pytest.raises(ValidationError):
        m.ReadinessCase.model_validate(data)


def test_dependency_cycle_rejected():
    m, _ = modules()
    a = requirement(depends_on=["b"])
    b = dict(id="b", label="B", category="zoning", expected=True, depends_on=["access"])
    with pytest.raises(ValidationError):
        m.ReadinessCase.model_validate(case_dict([a, b]))


def test_new_evidence_changes_memo_and_actions():
    _, e = modules()
    before = evaluate(case_dict())
    after = evaluate(case_dict(evidence=[record()]))
    changes = e.diff_reports(before, after)
    assert any(c.field == "decision" for c in changes)
    assert any(c.requirement_id == "access" for c in changes)
    assert after.actions == []


def test_memos_for_different_sites_cannot_be_compared():
    _, e = modules()
    before = evaluate(case_dict())
    data = case_dict()
    data["site_id"] = "other"
    after = evaluate(data)
    with pytest.raises(ValueError, match="same site"):
        e.diff_reports(before, after)


def test_changing_proposed_use_cannot_reuse_old_clearance():
    data = case_dict(evidence=[record()])
    data["intended_use"] = "Data center"
    assert evaluate(data).decision == "hold"


def test_unbounded_numeric_input_rejected_before_float_conversion():
    m, _ = modules()
    req = dict(id="area", category="site_identity", label="Area", expected=10**400,
               comparison="gte", unit="acre")
    with pytest.raises(ValidationError):
        m.ReadinessCase.model_validate(case_dict([req]))


def test_empty_critical_scope_cannot_be_reported_ready():
    m, _ = modules()
    req = requirement()
    req["critical"] = False
    with pytest.raises(ValidationError):
        m.ReadinessCase.model_validate(case_dict([req]))


def test_evidence_without_proposed_use_scope_never_clears():
    result = evaluate(case_dict(evidence=[record(intended_use=None)]))
    assert result.decision == "hold"
    assert "missing_use_scope" in result.findings[0].issues
