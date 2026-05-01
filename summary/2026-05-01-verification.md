# 2026-05-01 — Verification evidence (post exec-summary doc update)

Branch: `codex/dev-branch-pipeline`  
Commit verified: `c221e4c`

This file records the verification lanes rerun after the executive-summary documentation updates.

## Backend (repo root)

- Ruff (passed)
  - Command: `./.venv/bin/ruff check plotlot/src plotlot/tests plotlot/scripts`
  - Result: `All checks passed!`
- Unit tests (passed)
  - Command:
    - `env PYTHONPATH=plotlot/src MLFLOW_TRACKING_URI=file:///tmp/plotlot-mlruns ./.venv/bin/python -m pytest plotlot/tests/unit -q`
  - Result: `780 passed, 1 warning` (MLflow filesystem-store deprecation warning)

## Frontend (`plotlot/frontend`)

- Lint (passed with warnings)
  - Command: `npm run lint`
  - Result: `0 errors, 9 warnings`
- Typecheck (passed)
  - Command: `npx tsc --noEmit`
- UI unit tests (passed)
  - Command: `npm run test:ui`
  - Result: `10 passed`
- Production build (passed)
  - Command: `npm run build`

## E2E (Playwright)

Not rerun in this lane. Use:

- `make live-agent-e2e` (served frontend + backend; requires live creds)
- `make verify-local-no-browser` (deterministic gate without browser tests)
