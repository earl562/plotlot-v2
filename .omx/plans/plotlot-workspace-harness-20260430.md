# PlotLot Workspace Harness Plan

Date: 2026-04-30
Mode: planning only; no product implementation yet

## Current codebase facts

- PlotLot project root: `/Users/earlperry/Desktop/Projects/EP/plotlot`.
- Git isolation issue: `plotlot` is not currently its own Git repository. `git rev-parse --show-toplevel` resolves to `/Users/earlperry`, active branch `dev`; `git ls-files -- Desktop/Projects/EP/plotlot` returns no tracked files. A project-local branch requires first creating or attaching a project-local Git repo, or using a true existing PlotLot remote if one exists.
- Backend: FastAPI app mounts core routers in `src/plotlot/api/main.py:163-199`; expensive analysis/chat are rate-limited by middleware in `src/plotlot/api/main.py:148-160`.
- Existing direct analysis surface: `POST /api/v1/analyze` in `src/plotlot/api/routes.py:75-112` and streamed analysis in `src/plotlot/api/routes.py:120-180` onward.
- Current pipeline: `lookup_address` performs deterministic geocode/property/ordinance search, LLM extraction, then deterministic density math in `src/plotlot/pipeline/lookup.py:114-308`.
- Current chat harness: `src/plotlot/api/chat.py` is 1,792 lines and contains in-memory sessions, tool declarations, intent routing, tool execution, and SSE streaming. Dynamic tool masking exists in `src/plotlot/api/chat.py:896-929`, and raw tool dispatch is centralized in `src/plotlot/api/chat.py:1504-1557`.
- Existing high-risk external writes: Google Sheets/Docs are created and link-shared directly in `src/plotlot/retrieval/google_workspace.py:118-175` and `src/plotlot/retrieval/google_workspace.py:190-241`; chat can call these via `create_spreadsheet`, `create_document`, and `export_dataset` in `src/plotlot/api/chat.py:1535-1555`.
- Current persistence: SQLAlchemy models cover ordinance chunks, ingestion checkpoints, portfolio entries, report cache, and subscriptions in `src/plotlot/storage/models.py:13-148`; workspace/project/site/evidence/governance objects do not exist yet.
- API schemas currently center around address analysis, reports, docs, chat, portfolio, and geometry in `src/plotlot/api/schemas.py:10-309`.
- Frontend: `frontend/src/app/page.tsx` is 1,035 lines and owns mode, chat, local sessions, streaming, reports, document canvas, and lookup flows (`frontend/src/app/page.tsx:101-535`, render surface continues through `frontend/src/app/page.tsx:581-1035`).
- Frontend already has a sidebar/session shell (`frontend/src/app/SidebarLayout.tsx:12-108`, `frontend/src/components/Sidebar.tsx:21-225`) and a typed API client (`frontend/src/lib/api.ts:8-230`).
- Test surfaces exist for backend unit/eval/integration tests under `tests/`, frontend Vitest/Playwright tests under `frontend/tests/`, and scripts are defined in `pyproject.toml:1-73` and `frontend/package.json:1-43`.

## Alignment summary

We should not attempt the full PRD in one branch as a big-bang rewrite. The right first feature branch should build the durable harness spine around the existing working MVP while preserving current lookup/chat/report behavior.

The first branch should deliver **Phase 1 + a thin Phase 2 shell seam**:

1. Project-local Git isolation.
2. Repo-owned specs and contracts.
3. Backend harness core modules with typed inputs/outputs.
4. Governance middleware around existing tool execution.
5. Evidence ledger data model and recording path for current zoning analysis.
6. Workspace/project/site/analysis primitives and routes.
7. Frontend workspace shell scaffolding that can coexist with the current page.
8. Golden fixtures and tests that lock current behavior before refactors.

## Non-goals for this first branch

- No Gmail/Calendar/Drive sync UI beyond governance-safe contracts and existing Google write wrappers.
- No full CRM connector.
- No sandbox container runtime yet; only interfaces/contracts and approval gates.
- No model-provider migration unless necessary to route existing calls through a small model gateway adapter.
- No massive page redesign before behavior is locked.
- No public MCP implementation before internal tool contracts are stable.

## Branch strategy

Recommended isolation path:

1. Do **not** use the `/Users/earlperry` parent Git repository as the feature branch. It tracks the home directory context and does not currently track PlotLot.
2. Create a PlotLot-local Git repo or attach the intended existing PlotLot remote.
3. Add a root `.gitignore` before first commit to exclude `.env`, `.venv`, caches, local DBs, `mlruns`, `logs`, Playwright output, and generated artifacts.
4. Commit the current clean baseline.
5. Create branch `feature/plotlot-workspace-harness` from that baseline.

If an existing remote repo should be used instead, replace steps 2-4 with cloning/checking out that repo and applying this plan there.

## Proposed architecture slice

### Backend package layout

```text
src/plotlot/harness/
  __init__.py
  contracts.py              # Pydantic contracts for runtime, tools, skills, governance
  runtime.py                # HarnessRuntime orchestration facade
  skills.py                 # SkillRegistry and repo-owned manifest loading
  context.py                # ContextBroker + memory budget tiers
  governance.py             # GovernanceMiddleware, risk classes, approval decisions
  evidence.py               # EvidenceLedger service API
  model_gateway.py          # provider profile interface around existing LLM call path
  tool_gateway.py           # typed tool registry wrapping existing deterministic functions

src/plotlot/workspace/
  __init__.py
  schemas.py                # workspace/project/site/task/document/contact contracts
  service.py                # workspace application service

src/plotlot/api/workspace.py
src/plotlot/api/harness.py
```

### Database additions

Add migrations incrementally rather than one giant migration:

1. `007_workspaces_projects_sites.py`
   - `workspaces`
   - `workspace_members`
   - `projects`
   - `project_branches`
   - `sites`
2. `008_analysis_evidence_runs.py`
   - `analyses`
   - `analysis_runs`
   - `tool_runs`
   - `model_runs`
   - `evidence_items`
3. `009_reports_documents_tasks_crm.py`
   - `reports`
   - `documents`
   - `tasks`
   - `contacts`
   - `companies`
   - `opportunities`
4. `010_connections_memory_governance.py`
   - `workspace_connections`
   - `connector_sync_jobs`
   - `email_threads`
   - `calendar_events`
   - `drive_files`
   - `crm_records`
   - `workspace_memories`
   - `model_gateway_profiles`
   - `approval_requests`

### Harness execution path

Initial target path:

```text
/api/v1/projects/{project_id}/run
  -> HarnessRuntime.run(skill="zoning_research")
  -> ContextBroker builds LOW/MID context
  -> SkillRegistry resolves zoning_research manifest
  -> ToolGateway wraps existing geocode/property/search/calculator calls
  -> GovernanceMiddleware classifies tools and approval needs
  -> EvidenceLedger records facts/sources/tool/model runs
  -> existing ZoningReportResponse-compatible payload returned/streamed
```

The existing `/api/v1/analyze`, `/api/v1/analyze/stream`, and `/api/v1/chat` should keep working during this branch. New harness routes can call into existing functions first; only later should existing routes be moved behind the runtime.

## Implementation sequence

### Step 0 — Baseline and branch safety

- Establish project-local Git isolation using the branch strategy above.
- Add root `.gitignore` if needed.
- Run baseline checks and capture known failures:
  - `uv run pytest tests/unit -q`
  - `npm run lint` in `frontend/`
  - `npm run test:ui` in `frontend/`
  - targeted e2e no-db when servers are available: `npm run test:e2e:no-db`

Acceptance:
- PlotLot work happens on `feature/plotlot-workspace-harness` or equivalent isolated branch.
- Baseline test status is recorded before source changes.

### Step 1 — Repo-owned planning/spec artifacts

Create:

```text
docs/prd/plotlot-workspace-harness.md
docs/architecture/harness-runtime.md
docs/architecture/governance.md
docs/connector-contracts/google-workspace.md
docs/connector-contracts/gis-opendata.md
docs/skills/zoning_research.md
docs/skills/site_selection.md
docs/agents/zoning_analyst.yaml
docs/agents/evidence_reviewer.yaml
docs/evals/plotlot-bench.md
docs/runbooks/harness-release-gate.md
```

Acceptance:
- Docs translate the pasted PRD into repo-owned artifacts.
- Each planned runtime object has a typed contract or explicit deferred status.
- No implementation claims exist without a test/eval path.

### Step 2 — Contracts and manifests before behavior changes

Add Pydantic contracts for:

- `SkillManifest`
- `AgentManifest`
- `ToolCallRequest`
- `ToolCallResult`
- `ToolRiskClass`
- `GovernanceDecision`
- `EvidenceItemCreate`
- `HarnessRunRequest`
- `HarnessRunEvent`
- workspace/project/site/analysis/report/document/task records

Acceptance:
- Unit tests validate manifest loading and rejected invalid manifests.
- Contracts map to the PRD’s risk classes: `READ_ONLY`, `EXPENSIVE_READ`, `WRITE_INTERNAL`, `WRITE_EXTERNAL`, `EXECUTION`.

### Step 3 — Governance middleware around current tools

Wrap existing chat/tool calls through `GovernanceMiddleware` without changing user-facing behavior for safe tools.

Initial policy:

- Auto-allow: geocode, property lookup, ordinance search, evidence query.
- Audit-only first, then approval-gated: bulk property search, live GIS discovery, Drive/document parsing.
- Approval-required/block-by-default: Google Doc/Sheet creation, dataset export to Sheets, CRM writes, calendar/email sends, sandbox execution.

Acceptance:
- Existing tests for chat tools still pass after adapting mocks.
- New tests prove a prompt-injected Gmail/source text cannot trigger `send_email` or external write.
- `create_document`, `create_spreadsheet`, and `export_dataset` produce an approval request unless explicitly allowed in test policy.

### Step 4 — Evidence ledger and run records

Add evidence/tool/model run persistence and service methods.

Record evidence for current `lookup_address` stages:

- geocode result source and timestamp
- property record source/county/provider
- ordinance chunks/source refs
- extracted zoning claims
- deterministic calculation outputs

Acceptance:
- Running a zoning analysis creates linked `analysis_runs`, `tool_runs`, and `evidence_items`.
- Report claims can reference `evidence_item.id` or source refs.
- Tests verify required fields: `source_type`, `tool_name`, `retrieved_at`, confidence.

### Step 5 — Harness runtime facade

Introduce `HarnessRuntime` as a facade, not a rewrite.

Initial skills:

- `zoning_research`: wraps current `lookup_address` flow.
- `document_generation`: wraps existing clause builder but goes through governance.
- `site_selection`: manifest + stubbed contract only, unless minimal routing is cheap.

Acceptance:
- `HarnessRuntime.run(zoning_research)` returns a current-compatible report.
- Runtime emits structured stream events: `run_started`, `tool_started`, `tool_completed`, `evidence_recorded`, `approval_required`, `run_completed`, `run_failed`.
- Existing `/api/v1/analyze` can remain direct, but new `/api/v1/projects/{id}/run` uses runtime.

### Step 6 — Workspace/project/site API layer

Add API routes from the PRD subset:

```text
POST /api/v1/workspaces
GET  /api/v1/workspaces/{id}
GET  /api/v1/workspaces/{id}/projects
POST /api/v1/projects
GET  /api/v1/projects/{id}
POST /api/v1/projects/{id}/fork
POST /api/v1/projects/{id}/run
GET  /api/v1/projects/{id}/sites
GET  /api/v1/projects/{id}/evidence
GET  /api/v1/projects/{id}/reports
POST /api/v1/sites/{id}/analyze
POST /api/v1/approvals/{id}/approve
POST /api/v1/approvals/{id}/reject
```

Acceptance:
- Routes are auth/workspace-policy ready even if auth is still permissive locally.
- Route tests cover create/read/fork/run/evidence basics.
- All risky operations return approval state rather than executing directly.

### Step 7 — Frontend shell seam, not full redesign

Add a workspace route tree without breaking `/`:

```text
frontend/src/app/workspaces/[workspaceId]/page.tsx
frontend/src/app/projects/[projectId]/page.tsx
frontend/src/app/sites/[siteId]/page.tsx
frontend/src/features/workspace/
frontend/src/features/projects/
frontend/src/features/sites/
frontend/src/features/evidence/
frontend/src/features/reports/
frontend/src/features/harness/
```

Refactor only the safest seams first:

- `WorkspaceSidebar`
- `ProjectList`
- `SiteList`
- `EvidenceRail`
- `ExecutionTimeline`
- `ApprovalPanel`
- typed API client functions for new routes

Acceptance:
- Current home lookup/chat still passes existing UI tests.
- New workspace shell renders with fixture data and can show timeline/evidence events.
- No full extraction of `page.tsx` until tests lock its behavior.

### Step 8 — PlotLot-Bench seed

Create initial gold fixtures:

```text
plotlot-bench/router.jsonl
plotlot-bench/zoning_extraction.jsonl
plotlot-bench/evidence_validation.jsonl
plotlot-bench/report_generation.jsonl
plotlot-bench/security_injection.jsonl
```

Acceptance:
- At least 5 cases per file initially; structure supports 50-100 per stage later.
- A local eval runner validates shape and runs deterministic checks without external APIs.
- Existing `tests/eval` remains usable.

## Test plan

### Unit

- Manifest validation.
- Tool risk classification.
- Governance allow/block/approval decisions.
- Context budget routing LOW/MID/HIGH.
- Evidence item validation.
- Workspace/project/site service logic.
- Runtime event emission.

### Integration

- Workspace/project create/fork/run routes.
- Harness runtime wrapping `lookup_address` with mocked geocode/property/search/LLM.
- Evidence ledger write/read path.
- Approval route lifecycle.
- Chat external-write tools blocked or approval-gated.

### Frontend

- Workspace shell renders.
- Project/site navigation.
- Evidence rail displays fixtures and live API payloads.
- Approval panel state transitions.
- Existing quick lookup/chat UI regression tests remain green.

### E2E

- Existing no-db smoke path remains green.
- New fixture-backed workspace path loads project, site, run timeline, and evidence rail.
- Security prompt injection fixture does not trigger external write.

### Observability

- Runtime emits correlation IDs and structured events.
- Tool/model/evidence run records contain enough data for failure review.
- Approval decisions are audit logged.

## Risks and mitigations

- **Risk: big-bang rewrite breaks working MVP.** Mitigation: facade first, keep existing routes working, add tests before moving behavior.
- **Risk: branch isolation is currently unsafe because PlotLot is not its own repo.** Mitigation: create/attach project-local repo before implementation; do not branch the home-directory repo for this work.
- **Risk: schema migration sprawl.** Mitigation: split migrations into small reversible sets and keep services thin.
- **Risk: governance blocks existing happy paths unexpectedly.** Mitigation: audit-only for reads, explicit test policy overrides, staged enforcement for external writes.
- **Risk: frontend refactor scope creep.** Mitigation: add workspace routes/shell first; postpone monolith extraction until behavior is locked.
- **Risk: evidence ledger becomes write-only paperwork.** Mitigation: make report/evidence routes and EvidenceRail consume it in the same branch.

## Definition of done for first feature branch

- Separate branch/workspace isolation exists and is documented.
- Repo-owned specs under `docs/` exist.
- Harness contracts, governance, evidence, runtime facade, and workspace API subset are implemented with tests.
- Current lookup/chat/report behavior remains green or known failures are documented.
- Existing high-risk external writes are no longer executed directly by agent tool calls without governance decision.
- Frontend workspace shell can display projects/sites/evidence/timeline without replacing the current home flow.
- Seed PlotLot-Bench fixtures exist with deterministic validation.

## Open alignment item

The only blocker before implementation is Git isolation: PlotLot is currently untracked inside a parent home-directory Git repo. Recommended default is to initialize/attach a project-local PlotLot repo, commit a safe baseline, then create `feature/plotlot-workspace-harness`.
