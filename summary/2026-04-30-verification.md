# 2026-04-30 — Verification evidence (agentic harness milestone)

Branch: `codex/dev-branch-pipeline`  
Commit verified: `fa9f99e`

This file records the verification lanes run for the milestone delivered on 2026-04-30.

## Backend

- Ruff (passed)
  - Command: `./.venv/bin/ruff check plotlot/src plotlot/tests plotlot/scripts`
- Unit tests (passed)
  - Command:
    - `PYTHONPATH=plotlot/src MLFLOW_TRACKING_URI=file:///tmp/plotlot-mlruns ./.venv/bin/python -m pytest plotlot/tests/unit -q`
  - Result: `779 passed` (1 warning from MLflow filesystem store deprecation)

## Frontend (`plotlot/frontend`)

- Install dependencies (passed)
  - Command: `npm install`
- Lint (passed with warnings)
  - Command: `npm run lint`
  - Result: 0 errors, 9 warnings (existing code warnings; not introduced blockers)
- Typecheck (passed)
  - Command: `npx tsc --noEmit`
- UI unit tests (passed)
  - Command: `npm run test:ui`
- Production build (passed)
  - Command: `npm run build`

## E2E (Playwright)

- In this Codex sandbox, served E2E is blocked by a port-bind restriction:
  - Attempted: `npx playwright test tests/sidebar-navigation.spec.ts --project=chromium`
  - Failure: `listen EPERM: operation not permitted 127.0.0.1:3003`

Run Playwright on a normal dev machine per:

- `plotlot/docs/runbooks/tdd-local-success.md`
- `plotlot/scripts/run_live_agent_e2e.sh` (via `make live-agent-e2e`)

