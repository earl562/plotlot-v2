# Verification lanes

Select the lane matching the claim. Do not describe a fixture-based check as a
live property result.

| Claim | Run or observe | What it establishes |
| --- | --- | --- |
| Static frontend change | `cd plotlot/frontend && npm run lint && npx tsc --noEmit` | Lint and type status only |
| Backend logic change | `cd plotlot && uv run ruff check src/ tests/ && uv run pytest tests/unit/ -q` | Unit behavior on this checkout |
| Public UI and no-database navigation | `cd plotlot/frontend && npm run test:e2e:no-db` | Playwright's mocked/no-database scenario on port 3003 |
| Specific browser report | Start local app, follow `FEATURE_MAP.md`, click the relevant flow, inspect console/network and capture trace or screenshot | What the agent actually saw in this run |
| Backend availability | Start API, then `curl -fsS http://127.0.0.1:8000/health` | Current local health payload, not source-data completeness |
| Real estate fact | Inspect linked official record and reconcile identity, status, date, amount and conflicts | Only the precise claim supported by that record |

## Local ports

The root `README.md` documents frontend development at
`http://127.0.0.1:3000` and backend at `http://127.0.0.1:8000`:

```bash
cd plotlot
uv sync --frozen --dev --extra eval
uv run uvicorn plotlot.api.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
cd plotlot/frontend
npm ci
npm run dev -- --hostname 127.0.0.1 --port 3000
```

`plotlot/frontend/playwright.config.ts` defaults to **port 3003** and starts
its own build and server. Its `no-db` lane does not require the backend. For an
already running frontend, set `PLAYWRIGHT_BASE_URL` to its exact URL and
`PLAYWRIGHT_DISABLE_WEBSERVER=1`; verify that the intended process owns that
port. If 3003 is occupied by another project, choose a free test port with
`PLAYWRIGHT_PORT=3137` (or another available value) instead of reusing that
process. Do not point a test at a different local server by accident.

The database-backed and live-agent lanes require an appropriately configured
backend. Their Playwright preflight checks `/health`; a local no-db pass does
not satisfy those lanes. Keep test credentials and source exports out of git.

## Evidence record for each run

Record: checkout commit, commands and exit codes, lane, app URL and port,
scenario and input, observed UI/API output, trace or screenshot path, console
errors, source links when applicable, unresolved issues, and reviewer. Separate
`passed`, `failed`, `blocked`, and `not run`. A proposed test or an unexecuted
skill stays `not run`.
