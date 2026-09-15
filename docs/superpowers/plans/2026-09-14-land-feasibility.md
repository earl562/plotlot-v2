# Land Feasibility Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans to implement and verify
> each task in the isolated worktree. Keep main and cpt-pro unchanged.

**Goal:** Build an evidence-backed site-readiness preview and versioned saved case.
**Architecture:** Pure typed evaluation engine, transactional existing-table store,
FastAPI routes, and an internal browser workbench. No new runtime dependencies.
**Tech Stack:** Python, Pydantic 2, FastAPI, SQLAlchemy 2, vanilla browser JS.
**Spec:** docs/superpowers/specs/2026-09-14-land-feasibility-design.md

## Global Constraints
- Draft screening only; no professional certification or real-property clearance.
- User-supplied evidence remains labeled as such.
- No external actions, production deployment, DB migration, merge, or force push.
- New files live in the canonical plotlot/ workspace.
- A partial connector snapshot cannot establish full-repository regression status.

## Task 1: typed engine and playbooks
Files: `plotlot/src/plotlot/land_use/readiness/{__init__,models,engine,playbooks}.py`.
Tests: `plotlot/tests/unit/test_readiness_engine.py`.
Interface: `evaluate(case: ReadinessCase, *, today: date | None = None) -> ReadinessReport`.
- [x] Write failure cases for unknowns, contradictory records, invalid scope,
  staleness, future dates, invalid units, false/zero, and dependencies.
- [x] Observe a red run before implementing the missing engine.
- [x] Implement bounded contracts and deterministic findings/actions.
- [x] Verify fixture and validation tests; commit exact paths.

Example acceptance:
```python
report = evaluate(case_without_evidence, today=date(2026, 9, 14))
assert report.decision == "hold"
assert report.findings[0].status == "missing_evidence"
```

## Task 2: persistence and API
Files: `readiness/store.py`, `api/readiness.py`, and the existing `api/workspaces.py`.
Tests: `plotlot/tests/unit/test_readiness_api.py`, `test_readiness_store.py`.
Interface: `ReadinessStore(session).save(workspace_id, site_id, case,
expected_revision, actor_user_id)`; `load(workspace_id, site_id)`.
- [x] Write failing tests for unauthenticated/cross-tenant access, revision
  conflicts, parcel mismatch, unrelated-fact preservation, and audit snapshots.
- [x] Implement transaction-scoped version saves using existing sites/analysis_runs.
- [x] Add preview and scoped save/load routes; register through workspace router.
- [x] Test against an actual SQLite database with an asynchronous session adapter;
  explicitly distinguish that from PostgreSQL row-lock concurrency validation.

Example acceptance:
```python
saved = await store.save("w1", "s1", case, 0, "actor1")
assert saved.revision == 1
assert (await store.load("w1", "s1")).revision == 1
```

## Task 3: usable workbench and browser loop
Files: `readiness/workbench.html`, `plotlot/scripts/readiness_demo.py`,
`plotlot/tests/readiness_browser.py`.
- [x] Define browser assertions for unknown -> hold, demo contradiction -> hold,
  source-backed conflict -> do_not_proceed, import/export, and safe rendering.
- [x] Implement a workbench backed by the actual preview route, with explicit
  synthetic-demo labels and a structured evidence editor.
- [ ] Run browser assertions and inspect screenshot; correct defects and rerun.

## Task 4: checkpoint and verification
Files: `.github/workflows/land-feasibility.yml`, `plotlot/docs/SITE_READINESS.md`.
- [ ] Run all targeted tests, compilation and browser checks afresh.
- [ ] Inspect exact diff, secrets, integration blob and preserved base branch.
- [ ] Publish tested files to the isolated GitHub branch with the original base
  tree; record remote commit and any observed CI status.
- [ ] Deliver code bundle and explicit remaining validation limits.

## Checkpoint verification
- 74 targeted behavioral, persistence, and API tests pass in this runner.
- Python compilation and workbench JavaScript syntax checks pass.
- The browser suite was attempted against the real local API, but Chromium
  blocked localhost navigation (`ERR_BLOCKED_BY_ADMINISTRATOR`); browser
  assertions and visual inspection are not locally verified.
- Full-repository regressions, Next.js build, Ruff/mypy, PostgreSQL concurrency,
  deployed authentication, and live parcel/provider checks remain unverified.
- The dedicated GitHub workflow is supplied to exercise the browser suite in CI.
- Local worktree is a partial, verified connector snapshot. The GitHub feature
  branch is based on the complete cpt-pro commit a45afcc7f2527fe894ff9156576e863591be4bce.
