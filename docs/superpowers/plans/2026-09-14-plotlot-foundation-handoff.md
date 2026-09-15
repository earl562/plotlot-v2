# PlotLot Foundation: Plan and Implementation Handoff

## Status

The first foundation increment is implemented in an isolated local worktree and delivered as `PlotLot-Foundation-Implementation.zip` plus `PlotLot-Foundation-Changes.patch`. The complete product changes are NOT applied to this remote branch: the bulk publication step was blocked. This document is a handoff, not proof of remote implementation or successful full CI.

Base product commit: `c45de852dc02a2e3ac6536be915485dbc08276c2` (`cpt-pro` at inspection).
Local delivery commit: `8019d7663c660f7bf10a06042b8168e454dd3cf8`.
Patch SHA-256: `e812327dab1953e199ca4dd2ed442e28d08ba937a7385277e7d3c83c45898c2b`.

No merge to main, production deployment, production reingestion, live inference or customer writeback was performed. Do not use this remote branch's current CI results as evidence for the delivered implementation.

## Phased implementation plan

| Phase | Implemented locally | Next acceptance gate |
| --- | --- | --- |
| F1: Free-model reliability | Opt-in OpenRouter gateway, explicit free-model/provider policy, bounded attempts and deadlines, validated JSON/tool arguments, safe errors, shared LLM entry-point integration | Locked full CI, then bounded live-model checks with approved credentials, privacy policy and model allowlist |
| F2: Ingestion integrity | Section-aware snapshot parser, stable IDs and provenance, bounded active chunks, short-rule retention, vector alignment/shape checks; no silent truncation | Reviewed live source fixtures and complete active-path consolidation |
| F3: Retrieval and testing | Per-jurisdiction evaluator separating answerable retrieval, abstention and infrastructure errors; executable phase runner | Human-reviewed real-source benchmark and transactional candidate-index activation/rollback |
| F4: Integration process | Operator-only local plugin/skill package using the existing MCP server; field-mapping, permissions, approval and retry rollout contract | Live host verification, tenant-isolated customer sandbox and approved/idempotent writeback |
| F5: Story and recovery UX | Address-driven Lookup, preserved received progress/report during interruption, explicit incomplete-result language, guarded manual retry | Production build/Playwright and observed pilot-user comprehension |

## Fresh local verification

- Reliability: 101 passing Python tests, including existing LLM regressions.
- Ingestion: 79 passing Python tests, including existing parser/chunker regressions.
- Retrieval evaluator: 10 passing Python tests.
- Integration package and phase runner: 10 passing Python tests.
- Frontend Vitest: 50 passing tests across 13 files.
- Changed-file Ruff and limited changed-module type checks passed.
- Frontend TypeScript passed; ESLint reported zero errors and 21 warnings.
- `uv lock --check --offline` and Git whitespace checks passed.

The Python total is 200 focused tests, not 200 new tests or the full backend suite. Local Python runs used the explicit `--isolated` option, excluding project conftest/database integration. Full locked CI, the complete backend suite, production build and Playwright remain unverified.

## Apply and verify the delivered patch

Use a separate development worktree based on the base product commit above. Inspect the patch and run `git apply --check` before `git apply --index`. Do not force mismatched contexts or overwrite concurrent changes. The ZIP contains 43 changed source/document/test files, the exact patch, a hash manifest, the full plan/design/runbook and verification evidence.

After applying:

```bash
cd plotlot
uv sync --frozen --extra dev --extra eval
uv run python scripts/verify_foundation.py --phase all
uv run ruff check src/ tests/
uv run ruff format --check src/ tests/
uv run mypy src/plotlot/ --no-error-summary
uv run pytest tests/unit/ -v --tb=short
cd frontend
npm ci
npm run build
npm run test:e2e:no-db
```

The backend and database Playwright lanes require the repository's documented test database setup. Keep every unverified live/customer gate open until its actual evidence exists.

## Activation boundaries

Free inference is explicitly enabled with `PLOTLOT_LLM_PROVIDER=openrouter_free`, an operator-supplied `OPENROUTER_API_KEY`, and evaluated explicit `vendor/model:free` IDs in `OPENROUTER_FREE_MODELS`. There is no preselected model or live credential in the delivery. Legacy mode remains the default; switching back can re-enable configured paid providers and must not be automatic.

NVIDIA embeddings remain a separate provider dependency. The two ingestion paths are not fully consolidated; transactional index activation is not implemented. Interrupted UI state is not a durable recovery store. Existing local MCP tools may mutate sandbox data, and skills do not enforce tenant authorization. This increment is not a production-readiness certification.
