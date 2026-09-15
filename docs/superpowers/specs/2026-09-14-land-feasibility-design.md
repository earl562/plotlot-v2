# Land feasibility: site-readiness first slice

Approved direction: the user requested an isolated worktree and a build/test loop
following the site-readiness proposal in this conversation.

## Contract
A supplied site, development scenario, requirements, and structured evidence produce
an explicitly scoped DRAFT decision memo, risk register, and next-action plan.
No provider call or LLM is needed. Missing data is never a pass. A completed
checklist means READY_FOR_REVIEW, never certification or authorization to develop.

The first slice accepts structured source records, not raw-PDF interpretation.
Source-check flags describe the input user's review, not independent verification
by PlotLot. New source adapters, professional sign-off, costs, external messaging,
and automatic entitlement conclusions are out of scope.

## Architecture
- Strict Pydantic contracts bound payloads, numeric values, identifiers, and dates.
- A deterministic pure engine checks applicability, freshness, source provenance,
  scope, units, contradictions, requirements, and task dependencies.
- Reuse existing `sites.facts_json` for the latest version and `analysis_runs` for
  append-only input/output snapshots. No production schema change or migration.
- Tenant- and site-scoped API routes reuse the existing workspace router and
  authorization middleware. Persisted operations additionally require an actor.
- An internal, dependency-free browser workbench exercises the actual preview API.
  It is not a replacement for or a redesign of the main Next.js interface.

## Safety and acceptance
Critical conflict -> DO_NOT_PROCEED under this scenario. Critical uncertainty ->
HOLD. All critical requirements supported -> READY_FOR_REVIEW for the supplied
requirements only. Unknown optional items remain visible. False booleans and zero
must be preserved. Reject non-finite numbers, duplicate IDs, invalid dependency
references/cycles, and unknown fields. Evidence from another parcel/scenario,
stale or future-dated evidence, screening-only observations, and unit mismatches
cannot clear a critical requirement. Conflicting applicable evidence requires
resolution rather than a silent choice of the more favorable record.

Save requires matching authenticated tenant, stored site identity, and expected
revision. Lock the site row, update latest state, and append an AnalysisRun in a
single transaction. Do not overwrite unrelated facts. Never expose DB errors.

## Execution environment
Direct cloning/package downloads are blocked in this runner. A real git worktree
is created from a PARTIAL connector snapshot. The copied workspace integration
file is verified against remote blob faf495bab107122b15edfa5bed8ae770738c482d.
The GitHub feature branch is based on complete cpt-pro commit
`a45afcc7f2527fe894ff9156576e863591be4bce`; remote writes preserve its base tree.
Local targeted tests are not a full-repository baseline or production validation.
