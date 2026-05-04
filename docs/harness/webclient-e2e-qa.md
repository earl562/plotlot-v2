# Web Client E2E QA (Workspace + Live Tool Seams)

This checklist is the repo-owned, reproducible “does it work?” path for the PlotLot workspace web client — especially the **live Municode + ArcGIS/OpenData tool seams**.

## Start services

From repo root:

```bash
# backend (FastAPI)
cd apps/plotlot
./scripts/run_backend_with_codex_oauth.sh

# frontend (Next.js)
cd ../../
make frontend-dev
```

Open:
- Frontend: `http://127.0.0.1:3000/workspace`
- Backend: `http://127.0.0.1:8000/health`

## Visual smoke (recommended)

Run the Playwright UI seam test (captures screenshots):

```bash
cd apps/plotlot/frontend
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000 npx playwright test tests/agent-live-tools.spec.ts --project=chromium
```

Expected artifacts:
- `apps/plotlot/frontend/test-results/agent-live-tools-Agent-liv-93989-penData-Municode-live-tools-chromium/01-open-data-tool.png`
- `apps/plotlot/frontend/test-results/agent-live-tools-Agent-liv-93989-penData-Municode-live-tools-chromium/02-municode-tool.png`

## Manual E2E (browser-use CLI)

If you want interactive/manual clicks with saved screenshots from the terminal:

```bash
uvx "browser-use[cli]" doctor
uvx "browser-use[cli]" --session plotlot-e2e open http://127.0.0.1:3000/workspace
uvx "browser-use[cli]" --session plotlot-e2e state
uvx "browser-use[cli]" --session plotlot-e2e click <element-index>
uvx "browser-use[cli]" --session plotlot-e2e screenshot --full /private/tmp/plotlot-e2e.png
```

Tip: `state` prints interactable element indices, which you can pass to `click`.

## Backend seam checks (tool contracts + real invocations)

Tool contract inventory:

```bash
curl -fsS http://127.0.0.1:8000/api/v1/mcp/tools | jq -r '.tools[].name' | rg -i 'municode|open_data'
```

Expected:
- `plotlot.discover_open_data_layers`
- `plotlot.search_municode_live`

Invoke OpenData discovery (real ArcGIS/Hub call):

```bash
curl -fsS -X POST http://127.0.0.1:8000/api/v1/mcp/invoke \
  -H 'Content-Type: application/json' \
  -d '{"name":"plotlot.discover_open_data_layers","input":{"county":"Broward","state":"FL","lat":26.12,"lng":-80.14}}' \
  | jq -r '.status, .result.parcels_dataset.name, .result.zoning_dataset.name'
```

Invoke Municode live search (real Municode call):

```bash
curl -fsS -X POST http://127.0.0.1:8000/api/v1/mcp/invoke \
  -H 'Content-Type: application/json' \
  -d '{"name":"plotlot.search_municode_live","input":{"municipality":"Fort Lauderdale","query":"definitions"}}' \
  | jq -r '.status, .result.status, (.result.results[0].heading // "<no-heading>")'
```

## Notes on `$browser-use` (Codex in-app browser)

The `browser-use` skill expects a Codex-provided Node REPL tool (session metadata + image bridge).
If you see errors like:
- `Failed to connect to browser-use backend "iab"... No current Codex session metadata was available`
- `Failed to connect to browser-use backend "chrome"... native host is installed`

…use the Playwright UI seam test above as the repo-owned fallback evidence, and/or run the web client in a normal browser for manual interaction.
