from __future__ import annotations

import pytest

from plotlot.comps.florida_import import FloridaSDFCountyError, parse_florida_sdf

SDF_HEADER = (
    "CO_NO,PARCEL_ID,ASMNT_YR,ATV_STRT,GRP_NO,DOR_UC,NBRHD_CD,MKT_AR,CENSUS_BK,"
    "SALE_ID_CD,SAL_CHG_CD,VI_CD,OR_BOOK,OR_PAGE,CLERK_NO,QUAL_CD,SALE_YR,SALE_MO,"
    "SALE_PRC,MULTI_PAR_SAL,RS_ID,MP_ID,STATE_PARCEL_ID"
)


def _sdf_row(*, parcel_id: str, qualification: str, change: str, multi: str) -> str:
    return ",".join(
        (
            "23",
            parcel_id,
            "2026",
            "1",
            "1",
            "000",
            "ABC",
            "0",
            "0",
            "01",
            change,
            "V",
            "12345",
            "0067",
            f"CLERK-{parcel_id}",
            qualification,
            "2026",
            "02",
            "450000",
            multi,
            f"RS-{parcel_id}",
            "",
            f"23{parcel_id}",
        )
    )


def test_parse_florida_sdf_preserves_public_header_identity_and_month_precision() -> None:
    # Given: one official 23-column SDF row with a leading-zero parcel identifier.
    csv_text = "\n".join(
        (
            SDF_HEADER,
            "23,0012345678900,2026,1,1,000,ABC,0,0,01,00,V,12345,0067,"
            "2026000123,01,2026,01,450000,N,RS0001,,230012345678900",
        )
    )

    # When: the public Florida transfer file is parsed.
    candidates = parse_florida_sdf(
        csv_text,
        county="Miami-Dade",
        source_url="https://www.floridarevenue.com/property/dataportal/",
    )

    # Then: the transfer remains month-precise, reviewed-import evidence without spatial claims.
    candidate = candidates[0]
    assert candidate.parcel_id == "0012345678900"
    assert candidate.sale_date == "2026-01"
    assert candidate.date_precision == "month"
    assert candidate.sale_price == 450000.0
    assert candidate.category == "land"
    assert candidate.property_type == "land"
    assert candidate.qualification == "qualified"
    assert candidate.qualification_code == "01"
    assert candidate.source_kind == "user_reviewed"
    assert candidate.source_record_id == "RS0001"
    assert candidate.recorded_document == "CLERK 2026000123; OR 12345/0067"
    assert candidate.latitude is None
    assert candidate.longitude is None
    assert candidate.lot_size_sqft is None


def test_parse_florida_sdf_exposes_change_multiparcel_and_pending_qualification() -> None:
    # Given: DOR rows representing physical change, multi-parcel, and pending review.
    csv_text = "\n".join(
        (
            SDF_HEADER,
            _sdf_row(parcel_id="0000000000003", qualification="03", change="01", multi="N"),
            _sdf_row(parcel_id="0000000000005", qualification="05", change="00", multi="Y"),
            _sdf_row(parcel_id="0000000000099", qualification="99", change="00", multi="N"),
        )
    )

    # When: qualification fields cross the public SDF boundary.
    changed, multi, pending = parse_florida_sdf(
        csv_text,
        county="Miami-Dade",
        source_url="https://www.floridarevenue.com/property/dataportal/",
    )

    # Then: blocking conditions remain explicit while a pending code remains a closed transfer.
    assert changed.qualification == "qualified"
    assert changed.property_changed is True
    assert changed.conflict_flags == ("physical_change_after_transfer",)
    assert "SAL_CHG_CD=01" in changed.classification_basis
    assert multi.qualification == "disqualified"
    assert multi.multi_parcel is True
    assert multi.conflict_flags == ("unknown_sale_change_code", "multi_parcel_transaction")
    assert pending.qualification == "pending"
    assert pending.transaction_status == "closed"


def test_parse_florida_sdf_rejects_county_code_mismatch() -> None:
    # Given: a Miami-Dade code 23 row labeled by the caller as Broward.
    csv_text = "\n".join(
        (
            SDF_HEADER,
            _sdf_row(parcel_id="0000000000001", qualification="01", change="00", multi="N"),
        )
    )

    # When: the county label conflicts with the publisher's county code.
    with pytest.raises(FloridaSDFCountyError) as captured:
        parse_florida_sdf(
            csv_text,
            county="Broward",
            source_url="https://www.floridarevenue.com/property/dataportal/",
        )

    # Then: the parser reports the exact expected and actual county codes.
    assert captured.value.expected_code == "16"
    assert captured.value.actual_code == "23"
