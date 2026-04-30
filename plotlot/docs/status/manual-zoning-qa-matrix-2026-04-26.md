# Manual Zoning QA Matrix — 2026-04-26

Purpose: validate the deployed lookup lane with real South Florida addresses and classify each result as usable, weak, or failing before further agent refinement.

## Runtime baseline
- Local backend: reachable but DB-degraded (`database_unavailable`)
- Hosted backend: healthy, DB-backed analysis ready
- Hosted data-quality: 8,142 chunks across 5 seeded jurisdiction lanes

## Scenario results

| Address | Expected jurisdiction | Hosted result | Verdict | Notes |
| --- | --- | --- | --- | --- |
| 171 NE 209th Ter, Miami, FL 33179 | Miami Gardens / Miami-Dade | Municipality `Miami Gardens`, zoning `R-1`, owner present, ordinance-backed density analysis | Pass | Strongest current case; usable manual baseline |
| 7940 Plantation Blvd, Miramar, FL 33023 | Miramar / Broward | Municipality `Miramar`, zoning `RS5`, owner present, plausible numeric params | Pass with review | Looks grounded, but still flagged `medium` confidence |
| 6227 SW 19th St, West Miami, FL 33155 | West Miami / Miami-Dade | Municipality correct, zoning `R-1`, but `sources=[]` and "typical South Florida" assumptions | Weak | Not trustworthy until ordinance citations are real |
| 524 SW 5th Ave, Hallandale Beach, FL 33009 | Hallandale Beach / Broward | Municipality correct, zoning `RS-6`, but `sources=[]` and generic assumptions | Weak | Needs ordinance ingestion / retrieval correction |
| 1517 NE 5th Ct, Fort Lauderdale, FL 33301 | Fort Lauderdale / Broward | Returned mismatched property record/address and irrelevant admin/personnel sections | Fail | Indicates Broward parcel match and/or retrieval bug |

## Immediate conclusions
- Current hosted lookup is **not uniformly trustworthy** across municipalities.
- Miami Gardens and Miramar are the best current gold-path checks.
- West Miami and Hallandale Beach require ordinance coverage/retrieval improvements.
- Fort Lauderdale is an active correctness failure and should block any "working as intended" claim.

## Next validation targets
1. Re-test Fort Lauderdale after Broward parcel-match fix.
2. Re-test West Miami and Hallandale Beach after municipality-specific ordinance coverage improvements.
3. Keep Miami Gardens and Miramar as regression baselines for every lookup change.
