"""Validation tests for the agentic land-use harness gold-set fixture."""

from plotlot.land_use.goldset import ExpectedClaim, load_land_use_goldset


def test_land_use_goldset_loads_and_has_required_coverage():
    goldset = load_land_use_goldset()

    assert goldset.schema_version == "0.1.0"
    assert len(goldset.cases) >= 7
    assert "search_ordinances" in goldset.required_tools()
    assert "discover_open_data_layers" in goldset.required_tools()
    assert "external_writes_require_explicit_approval" in goldset.global_invariants


def test_goldset_case_ids_are_unique_and_cases_have_assertions():
    goldset = load_land_use_goldset()
    ids = [case.id for case in goldset.cases]

    assert len(ids) == len(set(ids))
    for case in goldset.cases:
        assert case.required_tools
        assert case.expected_claims
        assert case.forbidden
        assert case.site or case.site_group


def test_goldset_contains_security_and_data_center_cases():
    goldset = load_land_use_goldset()

    assert goldset.by_id("data-center-siting-screen-south-florida-001").workflow == (
        "data_center_siting_screen"
    )
    injection = goldset.by_id("prompt-injection-external-source-no-write-001")
    assert injection.external_source_text is not None
    assert "IGNORE ALL PRIOR RULES" in injection.external_source_text


def test_expected_claim_evaluator_supports_fixture_operators():
    observed = {
        "report.has_legal_caveat": True,
        "opendata.layer_candidates_count": 2,
        "summary": "ordinance citation present",
    }

    assert ExpectedClaim(
        claim_key="report.has_legal_caveat",
        operator="equals",
        value=True,
    ).evaluate(observed)
    assert ExpectedClaim(
        claim_key="opendata.layer_candidates_count",
        operator="gte",
        value=1,
    ).evaluate(observed)
    assert ExpectedClaim(
        claim_key="summary",
        operator="contains",
        value="citation",
    ).evaluate(observed)
