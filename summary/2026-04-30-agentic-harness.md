# 2026-04-30 — Agentic land‑use harness milestone (PlotLot)

Branch: `codex/dev-branch-pipeline`  
Delivery commit: `fa9f99e` (“Enable agentic land-use harness workflow in codex pipeline branch”)

## Goal

Evolve PlotLot from an “AI zoning identification app” into an **agentic land‑use / site‑feasibility consultant harness** with a governed workspace model:

`Workspace → Project → Site → Analysis → Evidence → Report → Document`

## What shipped

### Spec + architecture

- PRD + test spec for the harness direction, including API vs MCP vs tools vs skills tradeoffs, governance primitives, and testing layers:
  - `plotlot/.omx/plans/prd-agentic-land-use-harness.md`
  - `plotlot/.omx/plans/test-spec-agentic-land-use-harness.md`
- Architecture doc for the target harness (service boundaries, runtime, memory/evidence, connectors):
  - `plotlot/docs/architecture/agentic-land-use-harness.md`
- Golden fixture set for early agentic land-use evaluation:
  - `plotlot/tests/golden/land_use_cases.json`

### Backend: harness runtime + governance primitives

- Introduced harness runtime, tool registry, events, and policy/approval model:
  - `plotlot/src/plotlot/harness/*`
- Introduced land-use kernel primitives for evidence/citations/goldset:
  - `plotlot/src/plotlot/land_use/*`
- Added/expanded FastAPI routes for harness-shaped resources and tool adapters:
  - `plotlot/src/plotlot/api/{workspaces,analyses,evidence,tools,approvals,mcp}.py`
- Added DB migrations for harness tables:
  - `plotlot/alembic/versions/007_add_harness_core_tables.py`
  - `plotlot/alembic/versions/008_add_harness_artifact_connector_eval_tables.py`

### Frontend: clickable harness-shaped navigation + workspace routes

- Sidebar navigation made functional (not just visual) and aligned to harness primitives:
  - Added pages under `plotlot/frontend/src/app/(workspace)/` for `/analyses`, `/evidence`, `/reports`, `/connectors`, plus project/site routes.
- Added tests covering navigation and harness/workspace flows:
  - `plotlot/frontend/tests/sidebar-navigation.spec.ts`
  - `plotlot/frontend/tests/workspace-routes.no-db.spec.ts`

### Google Maps key not available → alternative added

- Implemented OpenStreetMap-based fallbacks (no API key required):
  - `plotlot/frontend/src/lib/mapAlternatives.ts`
  - Used by components like `SatelliteMap` / `ParcelViewer`.

### Runbooks + reproducible local success gate

- Deterministic local verification runbook:
  - `plotlot/docs/runbooks/tdd-local-success.md`
- Success gate script + Make targets:
  - `plotlot/scripts/verify_local_success.sh`
  - `plotlot/Makefile` targets: `verify-local`, `verify-local-no-browser`, `live-agent-e2e`, `mutation`, etc.
- Live served agent E2E runner (backend + Playwright):
  - `plotlot/scripts/run_live_agent_e2e.sh`

## Known limitations / constraints

- Some sandboxed environments disallow binding to loopback ports; in that case Playwright served E2E fails with `EPERM` when starting the dev server on `127.0.0.1:3003`. The runbook documents using `--skip-browser` for the deterministic gate and running Playwright on a normal dev machine.
- `uv sync` may fail in restricted environments due to cache permission constraints; the repo’s deterministic lane can use an existing `.venv` when present.

## Next steps (recommended)

- Run a full “served” E2E on a normal dev machine:
  - `cd plotlot && make live-agent-e2e`
- Iterate toward “trust-critical” harness readiness:
  - expand golden cases,
  - add more tool-contract coverage,
  - add mutation testing on the harness/policy/tool surfaces (`make mutation`).

