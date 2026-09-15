"""Synthetic SDF regressions; none of these rows represent real transactions."""

import csv
from io import StringIO

import pytest
from pydantic import ValidationError

from plotlot.comps.florida_import import FLORIDA_SDF_HEADER, parse_florida_sdf
from plotlot.comps.models import CompPolicy, CompSubject, SaleEvidence
from plotlot.comps.qualification_rules import assess_candidate


def imported_sale(change: str, qualification: str = "01") -> SaleEvidence:
    row = dict.fromkeys(FLORIDA_SDF_HEADER, "")
    row.update(
        CO_NO="23",
        PARCEL_ID="SYNTHETIC-COMP",
        QUAL_CD=qualification,
        SAL_CHG_CD=change,
        VI_CD="V",
        SALE_YR="2026",
        SALE_MO="02",
        SALE_PRC="100000",
        RS_ID="SYNTHETIC-RECORD",
        CLERK_NO="SYNTHETIC-DEED",
    )
    with StringIO(newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FLORIDA_SDF_HEADER)
        writer.writeheader()
        writer.writerow(row)
        return parse_florida_sdf(
            stream.getvalue(), "Miami-Dade", "https://example.invalid/synthetic-sdf"
        )[0]


@pytest.mark.parametrize("qualification", ("01", "02", "03"))
@pytest.mark.parametrize(
    "change", tuple(str(i) for i in range(1, 9)) + tuple(f"0{i}" for i in range(1, 9))
)
def test_significant_change_is_blocking_even_when_transfer_is_qualified(
    change: str, qualification: str
) -> None:
    # Given: an arm's-length transfer with a significant property change.
    # When: the change crosses the public SDF import boundary.
    candidate = imported_sale(change, qualification)
    # Then: transfer qualification is preserved independently from comparability.
    assert candidate.qualification == "qualified"
    assert candidate.property_changed is True
    assert "physical_change_after_transfer" in candidate.conflict_flags


@pytest.mark.parametrize("change", ("", " "))
def test_no_change_marker_does_not_invent_a_property_change(change: str) -> None:
    # Given / When: a row without a reported change is imported.
    candidate = imported_sale(change)
    # Then: no change is invented; spatial/at-sale/review evidence is still absent.
    assert candidate.property_changed is False
    assert candidate.conflict_flags == ()
    assert candidate.lot_size_sqft is None
    assert candidate.reviewed_by == ""


@pytest.mark.parametrize("change", ("0", "00", " 00 ", "9", "09", "x", "1.0", "-1"))
def test_unrecognized_change_code_requires_review(change: str) -> None:
    # Given / When: an unsupported source code is imported.
    candidate = imported_sale(change)
    # Then: it cannot silently become no-change evidence.
    assert "unknown_sale_change_code" in candidate.conflict_flags


@pytest.mark.parametrize("qualification", ("98", "99"))
def test_pending_qualification_remains_pending(qualification: str) -> None:
    # Given / When: a closed transfer awaiting qualification is imported.
    candidate = imported_sale("00", qualification)
    # Then: sale closure is independent of the pending qualification decision.
    assert candidate.qualification == "pending"
    assert candidate.transaction_status == "closed"


def test_imported_renovation_reaches_actual_comp_screening() -> None:
    # Given: otherwise eligible synthetic evidence, isolating only the change flag.
    subject = CompSubject(
        parcel_id="SYNTHETIC-SUBJECT",
        state="FL",
        county="Miami-Dade",
        latitude=25.77,
        longitude=-80.19,
        lot_size_sqft=10000,
    )
    policy = CompPolicy(as_of="2026-09-14")
    additions = {
        "latitude": 25.771,
        "longitude": -80.19,
        "lot_size_sqft": 10000,
        "reviewed_by": "Synthetic regression only",
        "reviewed_at": "2026-09-14",
    }
    unchanged = imported_sale("").model_copy(update=additions)
    renovated = imported_sale("07").model_copy(update=additions)
    # When: the actual downstream assessor evaluates the control and changed row.
    control = assess_candidate(subject, unchanged, policy)
    changed = assess_candidate(subject, renovated, policy)
    # Then: the imported change alone blocks the sale.
    assert control.reasons == ()
    assert set(changed.reasons) == {"property_changed_since_sale", "evidence_conflict"}


@pytest.mark.parametrize("cell_count", (22, 24))
def test_malformed_row_width_is_a_controlled_validation_error(cell_count: int) -> None:
    text = ",".join(FLORIDA_SDF_HEADER) + "\n" + ",".join([""] * cell_count)
    with pytest.raises(ValidationError):
        parse_florida_sdf(text, "Miami-Dade", "https://example.invalid/synthetic")
