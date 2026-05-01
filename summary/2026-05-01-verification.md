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

## Deterministic local success gate (no browser)

- `verify_local_success.sh` (passed)
  - Command: `cd plotlot && bash scripts/verify_local_success.sh --skip-browser`
  - Coverage: repo hygiene, backend ruff+unit, frontend lint+tsc+vitest, frontend production build

## Playwright browser lane (served Next dev server)

- Browser tests are **blocked in this Codex sandbox** due to a port bind restriction (`listen EPERM`).
- `scripts/verify_local_success.sh` now auto-detects this and **skips Playwright** when it can’t bind localhost ports.

Run browser E2E on a normal dev machine:
- `make verify-local` (includes Playwright design-system tests)
- `make live-agent-e2e` (served agent E2E; requires secrets)
