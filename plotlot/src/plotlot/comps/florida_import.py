from __future__ import annotations

import csv
from dataclasses import dataclass
from io import StringIO
from typing import Final, Iterator, TextIO

from pydantic import BaseModel, ConfigDict

from plotlot.comps.models import (
    CompCategory,
    DatePrecision,
    PropertyType,
    Qualification,
    SaleEvidence,
)

FLORIDA_SDF_HEADER: Final = (
    "CO_NO",
    "PARCEL_ID",
    "ASMNT_YR",
    "ATV_STRT",
    "GRP_NO",
    "DOR_UC",
    "NBRHD_CD",
    "MKT_AR",
    "CENSUS_BK",
    "SALE_ID_CD",
    "SAL_CHG_CD",
    "VI_CD",
    "OR_BOOK",
    "OR_PAGE",
    "CLERK_NO",
    "QUAL_CD",
    "SALE_YR",
    "SALE_MO",
    "SALE_PRC",
    "MULTI_PAR_SAL",
    "RS_ID",
    "MP_ID",
    "STATE_PARCEL_ID",
)
_COUNTY_CODES: Final = {
    "broward": "16",
    "miami-dade": "23",
    "palm beach": "60",
}
_OTHER_QUALIFICATIONS: Final[dict[str, Qualification]] = {
    "98": "pending",
    "99": "pending",
    "": "unknown",
}
_SIGNIFICANT_CHANGES: Final = frozenset(
    (*map(str, range(1, 9)), *(f"0{code}" for code in range(1, 9)))
)


@dataclass(frozen=True, slots=True)
class FloridaSDFHeaderError(ValueError):
    actual: tuple[str, ...]

    def __str__(self) -> str:
        return "Florida SDF must use the public 23-column publisher schema"


@dataclass(frozen=True, slots=True)
class FloridaSDFCountyError(ValueError):
    county: str
    expected_code: str
    actual_code: str

    def __str__(self) -> str:
        return (
            f"Florida SDF county mismatch for {self.county}: "
            f"expected {self.expected_code or 'a supported county'}, got {self.actual_code}"
        )


class FloridaSDFRow(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    CO_NO: str = ""
    PARCEL_ID: str = ""
    ASMNT_YR: str = ""
    ATV_STRT: str = ""
    GRP_NO: str = ""
    DOR_UC: str = ""
    NBRHD_CD: str = ""
    MKT_AR: str = ""
    CENSUS_BK: str = ""
    SALE_ID_CD: str = ""
    SAL_CHG_CD: str = ""
    VI_CD: str = ""
    OR_BOOK: str = ""
    OR_PAGE: str = ""
    CLERK_NO: str = ""
    QUAL_CD: str = ""
    SALE_YR: str = ""
    SALE_MO: str = ""
    SALE_PRC: str = ""
    MULTI_PAR_SAL: str = ""
    RS_ID: str = ""
    MP_ID: str = ""
    STATE_PARCEL_ID: str = ""


def _month(row: FloridaSDFRow) -> tuple[str, DatePrecision]:
    try:
        year = int(row.SALE_YR)
        month = int(row.SALE_MO)
    except ValueError:
        return "", "unknown"
    if year < 1900 or not 1 <= month <= 12:
        return "", "unknown"
    return f"{year:04d}-{month:02d}", "month"


def _price(value: str) -> float | None:
    cleaned = value.strip().replace("$", "").replace(",", "")
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _classification(row: FloridaSDFRow) -> tuple[PropertyType, CompCategory, str]:
    flag = row.VI_CD.strip().upper()
    basis = (
        f"Florida DOR VI_CD={flag or 'unknown'}; QUAL_CD={row.QUAL_CD.strip()}; "
        f"SAL_CHG_CD={row.SAL_CHG_CD.strip() or 'not_applicable'}"
    )
    return ("land", "land", basis) if flag == "V" else ("unknown", "unknown", basis)


def _qualification(code: str) -> Qualification:
    if code in {"01", "02", "03"}:
        return "qualified"
    return _OTHER_QUALIFICATIONS.get(code, "disqualified")


def _recorded_document(row: FloridaSDFRow) -> str:
    references: list[str] = []
    if row.CLERK_NO.strip():
        references.append(f"CLERK {row.CLERK_NO.strip()}")
    if row.OR_BOOK.strip() and row.OR_PAGE.strip():
        references.append(f"OR {row.OR_BOOK.strip()}/{row.OR_PAGE.strip()}")
    return "; ".join(references)


def _conflicts(row: FloridaSDFRow) -> tuple[str, ...]:
    conflicts: list[str] = []
    change = row.SAL_CHG_CD.strip()
    if row.QUAL_CD.strip() == "03" or change in _SIGNIFICANT_CHANGES:
        conflicts.append("physical_change_after_transfer")
    if change and change not in _SIGNIFICANT_CHANGES:
        conflicts.append("unknown_sale_change_code")
    multi_parcel = row.QUAL_CD.strip() == "05" or row.MULTI_PAR_SAL.strip().upper() in {
        "1",
        "Y",
        "YES",
    }
    if multi_parcel:
        conflicts.append("multi_parcel_transaction")
    return tuple(conflicts)


def _candidate(
    row: FloridaSDFRow,
    county: str,
    source_url: str,
    row_number: int,
) -> SaleEvidence:
    sale_date, precision = _month(row)
    property_type, category, basis = _classification(row)
    code = row.QUAL_CD.strip()
    multi_parcel = code == "05" or row.MULTI_PAR_SAL.strip().upper() in {"1", "Y", "YES"}
    record_id = row.RS_ID.strip()
    conflicts = _conflicts(row)
    return SaleEvidence(
        evidence_id=f"florida-sdf:{row.CO_NO.strip()}:{record_id or row_number}",
        parcel_id=row.PARCEL_ID.strip(),
        state="FL",
        county=county.strip(),
        sale_price=_price(row.SALE_PRC),
        sale_date=sale_date,
        date_precision=precision,
        property_type=property_type,
        category=category,
        classification_basis=basis,
        transaction_status="closed",
        qualification=_qualification(code),
        qualification_code=code,
        source_kind="user_reviewed",
        source_url=source_url,
        source_record_id=record_id,
        recorded_document=_recorded_document(row),
        multi_parcel=multi_parcel,
        property_changed="physical_change_after_transfer" in conflicts,
        conflict_flags=conflicts,
    )


def iter_florida_sdf_stream(
    stream: TextIO,
    county: str,
    source_url: str,
) -> Iterator[SaleEvidence]:
    """Stream the published SDF schema without retaining unrelated transfers."""
    reader = csv.DictReader(stream)
    actual_header = tuple(name.lstrip("\ufeff") for name in (reader.fieldnames or ()))
    if actual_header != FLORIDA_SDF_HEADER:
        raise FloridaSDFHeaderError(actual=actual_header)
    reader.fieldnames = list(actual_header)
    for row_number, raw_row in enumerate(reader, start=2):
        row = FloridaSDFRow.model_validate(raw_row)
        normalized_county = county.strip().casefold().removesuffix(" county").strip()
        expected_code = _COUNTY_CODES.get(normalized_county, "")
        actual_code = row.CO_NO.strip()
        if not expected_code or actual_code != expected_code:
            raise FloridaSDFCountyError(
                county=county,
                expected_code=expected_code,
                actual_code=actual_code,
            )
        yield _candidate(row, county, source_url, row_number)


def parse_florida_sdf_stream(
    stream: TextIO,
    county: str,
    source_url: str,
) -> tuple[SaleEvidence, ...]:
    return tuple(iter_florida_sdf_stream(stream, county, source_url))


def parse_florida_sdf(
    csv_text: str,
    county: str,
    source_url: str,
) -> tuple[SaleEvidence, ...]:
    with StringIO(csv_text, newline="") as stream:
        return parse_florida_sdf_stream(stream, county, source_url)
