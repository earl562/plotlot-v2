from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
from hashlib import sha256
from typing import Final

from pydantic import BaseModel, ConfigDict, HttpUrl, TypeAdapter, field_validator

from plotlot.comps.models import CompPolicy, CompSetResult, CompSubject, SaleEvidence
from plotlot.comps.qualification_rules import assess_candidate
from plotlot.comps.sources import SourceResult

LAUNCH_MARKETS: Final = frozenset(
    {
        ("FL", "Miami-Dade"),
        ("FL", "Broward"),
        ("FL", "Palm Beach"),
        ("FL", "Lee"),
        ("NC", "Mecklenburg"),
        ("NC", "Gaston"),
    }
)


class BenchmarkCase(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    subject: CompSubject
    identity_source_url: str
    expected_sales: tuple[SaleEvidence, ...] = ()

    @field_validator("identity_source_url")
    @classmethod
    def validate_identity_url(cls, value: str) -> str:
        TypeAdapter(HttpUrl).validate_python(value)
        return value


@dataclass(frozen=True, slots=True)
class BenchmarkRun:
    as_of: str
    source_status: str
    candidate_count: int
    accepted_ids: tuple[str, ...]
    rejection_counts: tuple[tuple[str, int], ...]
    evidence_fingerprint: str
    blockers: tuple[str, ...]
    source_urls: tuple[str, ...]
    source_notes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class BenchmarkSummary:
    state: str
    county: str
    address: str
    parcel_id: str
    identity_source_url: str
    repeatable: bool
    ready: bool
    blockers: tuple[str, ...]
    runs: tuple[BenchmarkRun, ...]


def assess_run(case: BenchmarkCase, source: SourceResult, result: CompSetResult) -> BenchmarkRun:
    blockers: list[str] = []
    if source.status != "available":
        blockers.append(f"source_{source.status}")
        if any(v is not None for v in (result.value_low, result.value_median, result.value_high)):
            blockers.append("value_from_incomplete_source")
    if result.status != "qualified" or len(result.accepted) < 3:
        blockers.append("insufficient_qualified_comps")
    expected_parcels = {sale.parcel_id for sale in case.expected_sales}
    if len(expected_parcels) < 3:
        blockers.append("missing_verified_sale_expectations")
    if len(expected_parcels) != len(case.expected_sales):
        blockers.append("duplicate_sale_expectations")
    policy = CompPolicy(as_of=result.as_of)
    for expected in case.expected_sales:
        try:
            reviewed = datetime.fromisoformat(expected.reviewed_at).date()
            review_valid = reviewed <= date.fromisoformat(result.as_of)
        except ValueError:
            review_valid = False
        if not (expected.reviewed_by.strip() and review_valid and expected.source_url.strip()):
            blockers.append("unreviewed_sale_expectation")
        if assess_candidate(case.subject, expected, policy).reasons:
            blockers.append(f"invalid_sale_expectation:{expected.evidence_id}")
        matches = tuple(
            sale
            for sale in result.accepted
            if sale.parcel_id == expected.parcel_id
            and sale.sale_date == expected.sale_date
            and sale.sale_price == expected.sale_price
            and sale.recorded_document == expected.recorded_document
            and sale.date_precision == expected.date_precision
            and sale.property_type == expected.property_type
            and sale.category == expected.category
            and sale.units == expected.units
            and sale.lot_size_sqft == expected.lot_size_sqft
            and sale.building_area_sqft == expected.building_area_sqft
        )
        if len(matches) != 1:
            blockers.append(f"expected_sale_mismatch:{expected.evidence_id}")
    if any(sale.parcel_id not in expected_parcels for sale in result.accepted):
        blockers.append("unexpected_accepted_sale")
    serialized = sorted(
        candidate.model_dump_json(exclude={"retrieved_at"}) for candidate in source.candidates
    )
    fingerprint = sha256("\n".join(serialized).encode()).hexdigest()
    reasons = Counter(reason for sale in result.rejected for reason in sale.reasons)
    return BenchmarkRun(
        as_of=result.as_of,
        source_status=source.status,
        candidate_count=len(source.candidates),
        accepted_ids=tuple(sorted(sale.evidence_id for sale in result.accepted)),
        rejection_counts=tuple(sorted(reasons.items())),
        evidence_fingerprint=fingerprint,
        blockers=tuple(sorted(set(blockers))),
        source_urls=source.source_urls,
        source_notes=source.notes,
    )


def summarize_case(case: BenchmarkCase, runs: tuple[BenchmarkRun, ...]) -> BenchmarkSummary:
    blockers = {blocker for run in runs for blocker in run.blockers}
    if len(runs) < 2:
        blockers.add("insufficient_repetitions")
    fingerprints = {
        (
            run.as_of,
            run.source_status,
            run.evidence_fingerprint,
            run.accepted_ids,
            run.rejection_counts,
            run.blockers,
            run.source_urls,
            run.source_notes,
        )
        for run in runs
    }
    repeatable = len(runs) >= 2 and len(fingerprints) == 1
    if not repeatable:
        blockers.add("results_not_repeatable")
    return BenchmarkSummary(
        state=case.subject.state,
        county=case.subject.county,
        address=case.subject.address,
        parcel_id=case.subject.parcel_id,
        identity_source_url=case.identity_source_url,
        repeatable=repeatable,
        ready=not blockers,
        blockers=tuple(sorted(blockers)),
        runs=runs,
    )
