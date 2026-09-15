# Repeatable real-property benchmark

This is a credential-free SDK benchmark, not a browser/sign-in test or a launch
approval. It calls the application's registered property providers and deterministic
comp qualifier, plus the standalone county adapters. Publication of these adapters
does not certify integration into every application pipeline. It does not
call an AI provider, write a database or use UniversalProvider discovery.

From the `plotlot` application directory:

```sh
PYTHONPATH=src .venv/bin/python -m plotlot.comps.benchmark_cli \
  --cases tests/fixtures/six-county-benchmark.json --as-of 2026-09-14
```

The evaluation date is explicit; policy is 3 miles, 12 months, minimum 3 comps,
maximum 5, 30% size tolerance. Each county runs twice, with a 25-second property
lookup and 45-second comp-fetch outer budget per repetition. County adapters have
their own tighter deadlines and row bounds. Six JSON lines expose counts,
accepted IDs, rejection reasons, source completeness, fingerprints, provenance,
and readiness blockers. Exit 0 requires every seed to pass; exit 1 means a
completed benchmark with unmet criteria; exit 2 means invalid CLI input.
Expected HTTP, source-payload and deadline errors become per-run blockers;
unexpected programming errors remain visible and may abort execution.

## What passing requires

- The app resolves the independently seeded parcel identity.
- Retrieval is complete, not partial, timed out or unsupported.
- At least three qualifying comps match independent reviewed expectations for
  parcel, price, date/precision, document, property type/category, units and area.
- No unexpected accepted parcels or duplicate expectation parcels.
- Two observations agree on source evidence and qualification decisions, ignoring
  retrieval timestamps only. Repeatability is not accuracy.

The checked-in seed manifest deliberately has **no approved comp expectations**.
Identity reference URLs are validated and emitted for audit, not fetched by this
command. Identity matching compares provider results against the independently
prepared seed; the command does not independently certify the seed itself.
We have not established independent, at-sale evidence packets for three suitable
sales per seed, and do not fabricate reviewer attestations to make tests pass.
Therefore the current real-data benchmark must fail readiness even if responses
are stable. Synthetic unit tests cover the passing/negative mechanics separately.

## Seed provenance and limits

| County | Property / parcel | Independent source and limitations |
| --- | --- | --- |
| Miami-Dade | 16 SE 2 ST / 0101000000020 | City parcel query in manifest; observed September 6. Current-area sources conflict; 92,972 sq ft is a diagnostic comparison input, not an approved legal area. |
| Broward | 532 NE 10 AVE / 504202030770 | County property table 36 plus parcel layer 16; September 5–6 observations. Area is GIS-derived. |
| Palm Beach | 224 DATURA ST / 74434321010060061 | Official property layer in manifest; September 5 observation. The site is an office building, not asserted vacant. |
| Lee | 1625 SE 39TH ST / 054524C4005440580 | Lee PropertySales layer 3, FOLIOID=10188356; September 14 matched STRAP. Approximate query point from polygon vertices, not a surveyed boundary. |
| Mecklenburg | 600 E 4TH ST / 12502601 | Official CAMA and ownership reconciliation in September 7 checkpoint; repeated through SDK September 14. Missing seed coordinates/area must be completed before its future sales adapter can be benchmarked. |
| Gaston | 128 W MAIN AVE / 105909 | Official PublicGIS/Parcels FeatureServer/11, PID='105909'; September 14 returned PIN 3545-88-5169, exact address and source latitude/longitude. |

The comparison question currently asks for land comps for each site, not whether
the subject is currently vacant. One seed per county is an initial diagnostic
baseline, not a representative release corpus. Expand with independently checked
land, resale, completed new-build, ambiguous-address, changed-property and
insufficient-data cases before claiming market readiness. San Diego is excluded.

## Saved live baseline, September 14, 2026

The [raw JSON lines](2026-09-14-six-county-baseline.jsonl) preserve both repetitions
for each county, including every emitted warning and readiness blocker.
Miami-Dade, Broward, Palm Beach and Mecklenburg resolved the expected parcel. Lee and Gaston could
not run dedicated identity lookups. All six failed readiness; no valuation was approved.
Miami-Dade returned a partial set then timed out; this correctly broke repeatability.
Earlier probes were stable, so they did not prove sustained reliability.

| County | Candidates per repetition | Accepted | Source result |
| --- | ---: | ---: | --- |
| Miami-Dade | 3,000 then 0 | 0 | partial then unavailable (timeout) |
| Broward | 1,877 | 0 | partial |
| Palm Beach | 3,797 | 0 | partial |
| Lee | 0 | 0 | unsupported; dedicated property provider also absent |
| Mecklenburg | 0 | 0 | unsupported sales route |
| Gaston | 0 | 0 | unsupported; dedicated property provider also absent |

These are emitted candidates, not independently verified sale counts. Required
historical lot area was absent from every candidate in the three FL feeds.
Current parcel size must not be substituted for transferred historical size.
The next data milestone is complete retrieval plus independent at-sale evidence,
not lowering qualification thresholds or moving to sign-in setup.
