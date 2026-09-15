# County retrieval repairs, September 14, 2026

Retrieval improved; the zero-approved-comp problem is **not resolved**. These are
credential-free SDK and benchmark CLI observations, not browser, deployed-app or
production-readiness certification. No qualification thresholds were weakened.

## Repairs and evidence

Miami-Dade checkpoint `c45de852dc02a2e3ac6536be915485dbc08276c2` restricts the parcel
query to the inclusive policy date window. For land, the vacant-sale flag must
belong to that same sale slot. All three historical slots remain available for
audit. The previous unfiltered three-mile query covered 84,844 parcels before a
1,000-parcel local cap; the date-and-vacant predicate matched 110. Three live SDK
observations returned 330 history entries in 0.904, 0.903 and 0.733 seconds without
timeouts. This does not establish a sustained availability guarantee.

The shared ArcGIS collector now advances a paginated query by the requested page
window rather than its returned row count. A Palm Beach request for 5,000 rows
returned 3,797: advancing by 3,797 overlapped 1,150 object IDs, while advancing by
5,000 did not. This follows the short-spatial-page behavior documented by
[Esri's query reference](https://developers.arcgis.com/rest/services-reference/enterprise/query-map-service-layer/).
Three repaired SDK observations retained 5,000 records in 1.964–2.295 seconds
without the repeated-page warning. They still correctly reported the local cap
as partial; underlying duplicate transactions were not declared resolved.

## Final isolated six-county run

[Raw results](2026-09-14-retrieval-repair.jsonl) were generated from staged tree
`2e8c7dbe5be4c6e898cc0b608ef02dea7119ee28`, based on the Miami checkpoint above.
The command used the checked-in six-county manifest and `--as-of 2026-09-14`.
It exited 1 because readiness criteria remain unmet, not because the CLI crashed.

| County | Candidates in each of two runs | Accepted | Source status |
| --- | ---: | ---: | --- |
| Miami-Dade | 330 | 0 | available, matching evidence fingerprints |
| Broward | 0 | 0 | unavailable, read timeout in both runs |
| Palm Beach | 5,000 | 0 | partial, local record cap |
| Lee | 0 | 0 | sales route and dedicated identity provider unsupported |
| Mecklenburg | 0 | 0 | sales route unsupported |
| Gaston | 0 | 0 | sales route and dedicated identity provider unsupported |

Every seed was repeatable in this run, but repeating a failure is not readiness.
The historical lot-size requirement failed every retrieved Miami-Dade and Palm
Beach candidate. Palm Beach also lacks supported at-sale category/type data.
All seeds still lack independent verified sale expectations. Current parcel area
cannot silently stand in for transferred area; price appreciation or visual
appearance cannot certify a new-build sale.

Remaining data work: establish independently reviewable historical sale packets,
complete Broward/Palm Beach retrieval, and implement verified Lee/Mecklenburg/
Gaston sales routes. A real acceptance property with trusted sale/deed evidence
is still needed. Sign-in and San Diego remain deferred.

## Verification scope

- Six new Miami query regressions failed before its fix and passed afterward.
- The short spatial-page regression failed before the cursor fix and passed afterward.
- Final isolated tree: **2,176 unit tests passed** in 19.61 seconds.
- Ruff checks passed; 479 files passed formatting; mypy passed 259 source files.
- One existing Starlette/httpx deprecation warning remains. LSP was unavailable;
  mypy and executed tests are the reported checks, not an LSP pass.
- Miami independent review: CLEAR/APPROVE on tree
  `e1196c900e2e6e58bc58ff7aa7ce0bafe9260e58`.
- Pagination independent review: CLEAR/APPROVE on tree
  `2e8c7dbe5be4c6e898cc0b608ef02dea7119ee28` against the Miami checkpoint.
- Only this receipt, raw observations and guide link were added after code testing.
- Earlier baseline GitHub CI failed its Repository Pair Release Gate while app
  quality and browser-test jobs passed; that separate gate was not repaired here.
  New checkpoint CI must be evaluated independently.

No model credits, production/shared database writes, deployment, sign-in changes,
debug listeners or persistent debug instrumentation were used. Unrelated dirty
pipeline and qualification work was excluded from the isolated checkpoint.
