# Florida SDF import boundary checkpoint

Scope: callable parser for the public 23-column Florida SDF, not an end-user
import UI, complete county comp pipeline, or production-readiness approval.

## Correctness

The [2026 Florida DOR standard, section 7](https://floridarevenue.com/property/Documents/2026FINALCompSubmStd.pdf#page=42)
defines significant change codes 1–8 even when transfer qualification is 01/02.
The parser now preserves those changes as blocking evidence. Padded 01–08 are
also blocked conservatively, not asserted to be valid submission encodings.
Blank is not-applicable; other nonblank encodings, including 0/00, require review.
Qualification 03 remains changed even without a change code. Qualification
98/99 is pending. No small-change value adjustment is attempted.

Source identity, exact codes, instrument references and month precision remain
intact. No sale-day area, coordinates, reviewer approval or completed-building
claim is invented. A valid header followed by surplus/missing data cells now
raises Pydantic validation errors instead of a surplus-cell AttributeError.

## Executed evidence

- Original failing-first change-code suite: 42 failed, 19 passed.
- Malformed-width regressions: two failed before the row-boundary repair.
- Final local parser plus CLI regression suite: 77 passed.
- Isolated candidate tree `4867a6b318457c157fe09b950e606dcb9121958c`:
  2,101 unit tests passed in 14.95 seconds; one existing Starlette/httpx warning.
- Full isolated Ruff check and 462-file format check passed. Changed source/test
  mypy passed. LSP unavailable; no LSP validation claim.
- Independent reviewer approved the exact candidate tree with no remaining
  findings after the CSV-width repair. Root retained the review in its local
  evidence ledger; that is not a full-release review.
- Actual parser-to-qualifier SDK driver: three otherwise eligible **synthetic**
  controls accepted; changing only SAL_CHG_CD to 07 rejected all three with
  `property_changed_since_sale` and `evidence_conflict`, withholding value.
  Unrecognized 00 also withheld value. These are software regression results,
  not real sales, human approvals or county coverage proof.

The six-county live benchmark remains a separate next checkpoint. Unrelated
local work is deliberately excluded. No paid model request, auth change,
deployment, production migration or San Diego expansion was performed.
