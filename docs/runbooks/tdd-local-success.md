# TDD Local Success Workflow

Use this runbook when implementing or debugging PlotLot changes locally. The goal is to keep every change inside a repeatable red/green/refactor loop and end with the same success gates that Ralph uses before completion.

## 1. Red: lock the failing behavior first

Before changing production code:

1. Identify the smallest observable behavior that should change.
2. Add or update the narrowest test that proves the behavior:
   - Backend pure logic/API contracts: `tests/unit/` with `pytest`.
   - Frontend components or API client logic: `frontend/tests/ui/` with Vitest.
   - Browser-visible flows: `frontend/tests/*.spec.ts` with Playwright.
   - Visual baseline changes: approved reference + Visual Verdict artifact under `.omx/artifacts/visual-ralph/`.
3. Run the focused test and confirm it fails for the expected reason.

Do not delete or weaken tests to get green.

## 2. Green: implement the smallest fix

Make the smallest code change that satisfies the failing test. Prefer existing utilities, tokens, and component boundaries. Avoid new dependencies unless the manifest already requires them or the dependency is explicitly approved.

Useful focused commands:

```bash
# Backend unit loop
MLFLOW_TRACKING_URI=file:///tmp/plotlot-mlruns uv run pytest tests/unit -q

# Backend lint loop
uv run ruff check src/ tests/ scripts/

# Frontend unit/type loop
cd frontend
npm run lint
npx tsc --noEmit
npm run test:ui

# Browser-visible design loop
npx playwright test tests/design-system.spec.ts --project=chromium
```

## 3. Refactor/deslop: clean only after green

After the focused test is green:

1. Remove dead code and unused imports introduced by the fix.
2. Collapse obvious duplication only inside the changed scope.
3. Keep visual changes stable after an approved reference; do not refactor styling that changes pixels unless Visual Verdict requires it.
4. Re-run the focused test immediately after cleanup.

## 4. Local success gate

Run the repo-native success gate before handing off or completing Ralph:

```bash
make verify-local
```

Equivalent direct command:

```bash
bash scripts/verify_local_success.sh
```

The default gate runs:

1. Repository hygiene check.
2. Backend ruff check.
3. Backend unit tests.
4. Frontend lint.
5. Frontend TypeScript check.
6. Frontend Vitest UI tests.
7. Frontend Playwright design-system tests.
8. Frontend production build.

If dependencies or browser binaries are missing, sync existing project toolchains first:

```bash
make install-local-tools
```

This uses only existing manifests: `uv sync --extra dev`, `npm install`, and `npx playwright install chromium`.

## 5. Narrow loops for fast debugging

Use flags to narrow the loop while debugging, then run the full gate before completion:

```bash
# Backend only
bash scripts/verify_local_success.sh --skip-frontend

# Frontend unit/type only; no browser or build
bash scripts/verify_local_success.sh --skip-backend --skip-browser --skip-build

# Browser skipped when sandbox cannot bind loopback; rerun with permission/escalation later
bash scripts/verify_local_success.sh --skip-browser
```

## 6. Known local caveats

- Playwright browser tests use `127.0.0.1:3003` by default to avoid reusing a stale developer server; override with `PLAYWRIGHT_PORT` or `PLAYWRIGHT_BASE_URL` when needed.
- Some sandboxed environments disallow binding to localhost ports. In that case Playwright lanes will fail with `EPERM` and you should rerun the gate with `--skip-browser`, then run Playwright on a normal dev machine.
- DB/live-service e2e tests are intentionally not part of the default local success gate. Run them explicitly when touching DB-backed or live-integration behavior.

## 7. Authenticated/live completion

Deterministic local success does not require external secrets. For live integrations, run the auth readiness checker:

```bash
make auth-readiness
python3 scripts/check_auth_readiness.py --json
```

See `docs/runbooks/authenticated-test-matrix.md` for the credential-to-test mapping. Use `--strict-auth` only when a task explicitly requires all live credential-backed lanes to be ready.

For a Kimi-style served web-agent proof, run:

```bash
make live-agent-e2e
```

That lane verifies the frontend is served by Playwright and the browser talks to the real `/api/v1/chat` SSE backend with live LLM credentials.

## 8. Mutation testing (optional QA lane)

Use mutation testing to validate that the test suite would catch subtle regressions in the harness/tool layer.

PlotLot uses `mutmut` for backend mutation testing. This is intentionally **not** part of the default local success gate because it is slow.

Run (recommended on macOS):

```bash
PYTHONFAULTHANDLER=1 uv run --python python3.12 --extra mutation --extra dev --extra mlflow mutmut run --max-children 1
```

Notes:

- On macOS, `mutmut` uses multiprocessing + `fork`, which can trigger `worker exit code -11` (SIGSEGV) depending on imports and concurrency.
- This repo sets `use_setproctitle = false` in `[tool.mutmut]` to avoid known fork-safety crashes.
- If you see widespread `-11` across many mutants, treat it as an infra problem (not a meaningful “killed mutant” result); reduce concurrency and narrow mutation scope.

Then inspect survivors (mutants that tests did not kill):

```bash
uv run mutmut results
uv run mutmut show <mutant_id>
```

Treat survivors as “missing assertion” signals and add tests (or document false positives) before release.
