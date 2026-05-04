# Objective.md integration audit (workspace-native harness seam)

This document maps the original `../objective.md` Phase goal to concrete, reviewable repo artifacts.

Scope: `pi-feature-branch` (PlotLot v2 monorepo).

## Harness foundation (objective steps)

### Step 1 — Harness contracts

- Code: `apps/plotlot/src/plotlot/harness/contracts.py`
- Unit coverage: `apps/plotlot/tests/unit/test_harness_foundation.py`

### Step 2 — Skill registry

- Code: `apps/plotlot/src/plotlot/harness/skill_registry.py`
- Unit coverage: `apps/plotlot/tests/unit/test_skill_registry.py`

### Step 3 — Harness runtime

- Code: `apps/plotlot/src/plotlot/harness/runtime.py`
- Unit coverage: `apps/plotlot/tests/unit/test_harness_runtime.py`

### Step 4 — Intent router

- Code: `apps/plotlot/src/plotlot/harness/router.py`
- Gold cases: `apps/plotlot/tests/gold/router_cases.jsonl`
- Unit coverage: `apps/plotlot/tests/unit/test_harness_router.py`

### Step 5 — Zoning research skill wrapper

- Code:
  - `apps/plotlot/src/plotlot/skills/zoning_research/workflow.py`
  - `apps/plotlot/src/plotlot/skills/zoning_research/schemas.py`
- Gold cases: `apps/plotlot/tests/gold/zoning_research_cases.jsonl`

### Step 6 — Skill runbook

- Runbook: `apps/plotlot/src/plotlot/skills/zoning_research/SKILL.md`

### Step 7 — Evidence recorder seam

- Minimal runtime seam: `apps/plotlot/src/plotlot/harness/evidence.py`
- Production evidence service: `apps/plotlot/src/plotlot/evidence.py`

### Step 8 — Workspace/project/site schemas

- Schemas: `apps/plotlot/src/plotlot/api/schemas_workspace.py`

### Step 9 — Harness API route

- API: `apps/plotlot/src/plotlot/api/harness.py`
- Router registration: `apps/plotlot/src/plotlot/api/main.py`
- Unit coverage: `apps/plotlot/tests/unit/test_harness_api.py`

### Step 10 — MCP scaffolding (thin adapter)

- API: `apps/plotlot/src/plotlot/api/mcp.py`
- Unit coverage: `apps/plotlot/tests/unit/test_mcp_api.py`

### Step 11 — Ordinance API scaffold

- API: `apps/plotlot/src/plotlot/api/ordinances.py`
- Gold cases: `apps/plotlot/tests/gold/ordinance_search_cases.jsonl`

### Step 12 — Gold-set tests

- Gold data:
  - `apps/plotlot/tests/gold/router_cases.jsonl`
  - `apps/plotlot/tests/gold/zoning_research_cases.jsonl`
  - `apps/plotlot/tests/gold/ordinance_search_cases.jsonl`

## Web-client tool seams (live Municode + ArcGIS/OpenData)

- Backend tool handlers:
  - `search_municode_live` in `apps/plotlot/src/plotlot/api/chat.py`
  - `discover_open_data_layers` in `apps/plotlot/src/plotlot/api/chat.py`
- UI entry points:
  - Tool cards: `apps/plotlot/frontend/src/components/ToolCards.tsx`
  - Workspace page: `apps/plotlot/frontend/src/app/workspace/page.tsx`
- UI verification (Playwright):
  - `apps/plotlot/frontend/tests/agent-live-tools.spec.ts`

## Quality / “production grade” gates (recently validated)

- Backend unit lane:
  - `make backend-lint`
  - `make backend-test`
- Frontend lanes:
  - `make frontend-lint`
  - `make frontend-build`
  - `npm run test:e2e:no-db`

