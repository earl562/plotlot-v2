from dataclasses import replace
from pathlib import Path

import pytest
import httpx
from pydantic import TypeAdapter, ValidationError

from plotlot.comps.benchmark import BenchmarkCase, assess_run, summarize_case
from plotlot.comps.models import CompPolicy, CompSubject, SaleEvidence
from plotlot.comps.qualification import qualify_comps
from plotlot.comps.sources import SourceResult


def test_repeatable_empty_results_do_not_pass_benchmark() -> None:
    # Given: a real-property seed without independently verified comp expectations.
    case = BenchmarkCase(
        subject=CompSubject(parcel_id="12502601", state="NC", county="Mecklenburg"),
        identity_source_url="https://meckgis.mecklenburgcountync.gov/",
    )
    source = SourceResult((), "unsupported", (), ())
    result = qualify_comps(case.subject, (), CompPolicy(as_of="2026-09-14"))
    # When: identical unsupported runs are summarized.
    run = assess_run(case, source, result)
    summary = summarize_case(case, (run, run))
    # Then: stability never substitutes for useful, verified comps.
    assert summary.repeatable is True
    assert summary.ready is False
    assert "missing_verified_sale_expectations" in summary.blockers
    assert "source_unsupported" in summary.blockers


def test_partial_source_never_passes_even_if_qualifier_reports_a_value() -> None:
    # Given: an incomplete county search and an erroneously valued downstream result.
    case = BenchmarkCase(
        subject=CompSubject(parcel_id="12502601", state="NC", county="Mecklenburg"),
        identity_source_url="https://meckgis.mecklenburgcountync.gov/",
    )
    source = SourceResult((), "partial", (), ())
    result = replace(
        qualify_comps(case.subject, (), CompPolicy(as_of="2026-09-14")),
        status="qualified",
        value_median=100000,
    )
    # When: the benchmark evaluates incomplete evidence.
    run = assess_run(case, source, result)
    # Then: a numeric answer does not hide the incomplete search.
    assert "source_partial" in run.blockers
    assert "value_from_incomplete_source" in run.blockers


def test_repeatability_requires_two_observations() -> None:
    # Given: only one observation.
    case = BenchmarkCase(
        subject=CompSubject(parcel_id="12502601", state="NC", county="Mecklenburg"),
        identity_source_url="https://meckgis.mecklenburgcountync.gov/",
    )
    run = assess_run(
        case,
        SourceResult((), "unavailable", (), ()),
        qualify_comps(case.subject, (), CompPolicy(as_of="2026-09-14")),
    )
    # When: a single run is summarized.
    summary = summarize_case(case, (run,))
    # Then: no repeatability claim is made.
    assert summary.repeatable is False
    assert "insufficient_repetitions" in summary.blockers


def verified_synthetic_case() -> BenchmarkCase:
    return BenchmarkCase(
        subject=CompSubject(
            parcel_id="SYNTHETIC-SUBJECT",
            state="FL",
            county="Broward",
            latitude=26.1,
            longitude=-80.1,
            lot_size_sqft=10000,
        ),
        identity_source_url="https://example.invalid/synthetic",
        expected_sales=tuple(
            SaleEvidence(
                evidence_id=f"SYNTHETIC-{i}",
                parcel_id=f"SYNTHETIC-{i}",
                state="FL",
                county="Broward",
                sale_date="2026-08-01",
                date_precision="day",
                sale_price=100000,
                category="land",
                property_type="land",
                lot_size_sqft=10000,
                latitude=26.101,
                longitude=-80.1,
                transaction_status="closed",
                qualification="qualified",
                qualification_code="01",
                classification_basis="Synthetic at-sale land evidence for QA only",
                source_kind="user_reviewed",
                source_url="https://example.invalid/synthetic",
                recorded_document=f"SYNTHETIC-{i}",
                reviewed_by="Synthetic QA only",
                reviewed_at="2026-09-14",
            )
            for i in range(3)
        ),
    )


def test_complete_matching_reviewed_expectations_can_pass() -> None:
    case = verified_synthetic_case()
    result = qualify_comps(case.subject, case.expected_sales, CompPolicy(as_of="2026-09-14"))
    run = assess_run(case, SourceResult(case.expected_sales, "available", (), ()), result)
    assert summarize_case(case, (run, run)).ready is True


def test_repeating_one_expected_sale_does_not_satisfy_three_comp_requirement() -> None:
    original = verified_synthetic_case()
    result = qualify_comps(
        original.subject, original.expected_sales, CompPolicy(as_of="2026-09-14")
    )
    duplicate = original.model_copy(update={"expected_sales": (original.expected_sales[0],) * 3})
    run = assess_run(duplicate, SourceResult(original.expected_sales, "available", (), ()), result)
    assert "duplicate_sale_expectations" in run.blockers
    assert "unexpected_accepted_sale" in run.blockers


def test_changed_source_price_breaks_repeatability() -> None:
    case = verified_synthetic_case()
    result = qualify_comps(case.subject, case.expected_sales, CompPolicy(as_of="2026-09-14"))
    first = assess_run(case, SourceResult(case.expected_sales, "available", (), ()), result)
    changed = (
        case.expected_sales[0].model_copy(update={"sale_price": 100001}),
        *case.expected_sales[1:],
    )
    second = assess_run(case, SourceResult(changed, "available", (), ()), result)
    assert summarize_case(case, (first, second)).repeatable is False


def test_only_retrieval_timestamp_changes_do_not_break_repeatability() -> None:
    case = verified_synthetic_case()
    result = qualify_comps(case.subject, case.expected_sales, CompPolicy(as_of="2026-09-14"))
    first = assess_run(case, SourceResult(case.expected_sales, "available", (), ()), result)
    changed = tuple(
        s.model_copy(update={"retrieved_at": "2026-09-14T20:00:00Z"}) for s in case.expected_sales
    )
    second = assess_run(case, SourceResult(changed, "available", (), ()), result)
    assert summarize_case(case, (first, second)).repeatable is True


def test_manifest_covers_six_real_identity_seeds_without_fabricated_comp_approvals() -> None:
    path = Path(__file__).parents[1] / "fixtures/six-county-benchmark.json"
    cases = TypeAdapter(tuple[BenchmarkCase, ...]).validate_json(path.read_bytes())
    assert {(c.subject.state, c.subject.county) for c in cases} == {
        ("FL", "Miami-Dade"),
        ("FL", "Broward"),
        ("FL", "Palm Beach"),
        ("FL", "Lee"),
        ("NC", "Mecklenburg"),
        ("NC", "Gaston"),
    }
    assert len(cases) == 6
    assert all(not c.expected_sales for c in cases)


@pytest.mark.asyncio
async def test_unsupported_county_never_uses_paid_universal_discovery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from plotlot.comps import benchmark_cli

    def forbidden_lookup(*args: str, **kwargs: str) -> None:
        pytest.fail("unsupported county must not use universal discovery")

    monkeypatch.setattr(benchmark_cli, "lookup_property", forbidden_lookup)
    case = BenchmarkCase(
        subject=CompSubject(
            parcel_id="105909", state="NC", county="Gaston", address="128 W MAIN AVE"
        ),
        identity_source_url="https://gis.gastoncountync.gov/",
    )
    summary = await benchmark_cli.run_case(case, CompPolicy(as_of="2026-09-14"))
    assert "identity_provider_unsupported" in summary.blockers
    assert "source_unsupported" in summary.blockers


def test_changed_source_warning_breaks_repeatability() -> None:
    case = verified_synthetic_case()
    result = qualify_comps(case.subject, case.expected_sales, CompPolicy(as_of="2026-09-14"))
    first = assess_run(case, SourceResult(case.expected_sales, "available", (), ()), result)
    second = replace(first, source_notes=("Historical area needs reconciliation.",))
    assert summarize_case(case, (first, second)).repeatable is False


@pytest.mark.parametrize("url", ["not a URL", "file:///tmp/source", "https://"])
def test_identity_reference_requires_http_url(url: str) -> None:
    with pytest.raises(ValidationError):
        BenchmarkCase(subject=verified_synthetic_case().subject, identity_source_url=url)


@pytest.mark.parametrize("reviewed_at", ["invalid", "2026-09-15"])
def test_county_expectations_need_valid_nonfuture_review(reviewed_at: str) -> None:
    original = verified_synthetic_case()
    sales = tuple(
        sale.model_copy(update={"source_kind": "county", "reviewed_at": reviewed_at})
        for sale in original.expected_sales
    )
    case = original.model_copy(update={"expected_sales": sales})
    result = qualify_comps(case.subject, sales, CompPolicy(as_of="2026-09-14"))
    run = assess_run(case, SourceResult(sales, "available", (), ()), result)
    assert "unreviewed_sale_expectation" in run.blockers


@pytest.mark.parametrize("boundary", ["lookup", "fetch"])
@pytest.mark.asyncio
async def test_operational_failure_preserves_both_runs(
    boundary: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    from unittest.mock import AsyncMock

    from plotlot.comps import benchmark_cli
    from plotlot.core.types import PropertyRecord

    case = verified_synthetic_case()
    lookup = AsyncMock(return_value=PropertyRecord(folio=case.subject.parcel_id))
    fetch = AsyncMock(return_value=SourceResult((), "available", (), ()))
    failing = lookup if boundary == "lookup" else fetch
    failing.side_effect = httpx.ConnectError("synthetic unavailable source")
    monkeypatch.setattr(benchmark_cli, "lookup_property", lookup)
    monkeypatch.setattr(benchmark_cli, "fetch_county_candidates", fetch)
    summary = await benchmark_cli.run_case(case, CompPolicy(as_of="2026-09-14"))
    assert len(summary.runs) == 2
    assert lookup.await_count == fetch.await_count == 2
    assert summary.ready is False
    assert (
        "identity_unavailable" if boundary == "lookup" else "source_unavailable"
    ) in summary.blockers
    assert summary.identity_source_url == case.identity_source_url


@pytest.mark.parametrize("boundary", ["lookup", "fetch"])
@pytest.mark.asyncio
async def test_programming_value_error_propagates(
    boundary: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    from unittest.mock import AsyncMock

    from plotlot.comps import benchmark_cli
    from plotlot.core.types import PropertyRecord

    case = verified_synthetic_case()
    lookup = AsyncMock(return_value=PropertyRecord(folio=case.subject.parcel_id))
    fetch = AsyncMock(return_value=SourceResult((), "available", (), ()))
    failing = lookup if boundary == "lookup" else fetch
    failing.side_effect = ValueError("synthetic programming defect")
    monkeypatch.setattr(benchmark_cli, "lookup_property", lookup)
    monkeypatch.setattr(benchmark_cli, "fetch_county_candidates", fetch)
    with pytest.raises(ValueError, match="synthetic programming defect"):
        await benchmark_cli.run_case(case, CompPolicy(as_of="2026-09-14"))
