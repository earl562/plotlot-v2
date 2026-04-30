# PRD — PlotLot Workspace Harness First Feature Branch

Date: 2026-04-30
Owner: Ralph execution loop
Source plan: `.omx/plans/plotlot-workspace-harness-20260430.md`

## Problem

PlotLot has a strong zoning-analysis MVP, but the core product should evolve from an AI zoning app into a governed, evidence-backed, workspace-native land-use and site-feasibility harness. The current codebase lacks first-class workspace/project/site/evidence/governance/runtime primitives, and the frontend home page/chat backend concentrate too many responsibilities in monolithic files.

## Goal

Deliver the first feature-branch slice that creates the durable harness spine while preserving current MVP behavior.

## User outcomes

1. A user can work inside a PlotLot workspace/project/site abstraction rather than only ad hoc local sessions.
2. A zoning/site analysis can be represented as a durable run with evidence and tool/model traceability.
3. Risky actions are governed by runtime policy rather than being directly executed by model tool calls.
4. Engineers can iterate on repo-owned specs, skills, contracts, and gold fixtures in reviewable files.
5. Existing lookup/chat/report flows continue to work while the new runtime is introduced behind stable seams.

## Scope for first branch

### Must ship

- Clean project-local Git baseline and `feature/plotlot-workspace-harness` branch.
- Root `.gitignore` protecting secrets and generated/runtime artifacts.
- Repo-owned docs/spec directories for PRD, architecture, skills, agents, runbooks, evals, and connector contracts.
- Harness contracts for skills, agents, tools, governance, evidence, runtime events, and workspace objects.
- Governance middleware with risk classes: `READ_ONLY`, `EXPENSIVE_READ`, `WRITE_INTERNAL`, `WRITE_EXTERNAL`, `EXECUTION`.
- Evidence ledger and run-record data model/services.
- `HarnessRuntime` facade that initially wraps current zoning analysis rather than rewriting it.
- Workspace/project/site API subset.
- Frontend workspace shell seam with project/site/evidence/timeline/approval components or fixtures.
- Seed `plotlot-bench` fixtures and deterministic validation.
- Tests covering contracts, governance, evidence, workspace routes, runtime facade, and frontend shell.

### Must preserve

- Existing `/api/v1/analyze`, `/api/v1/analyze/stream`, `/api/v1/chat`, portfolio, document, geometry, and render behavior unless explicitly wrapped with backward-compatible governance.
- Existing frontend `/` lookup and agent modes.

### Non-goals for first branch

- Full Gmail/Calendar/Drive sync UI.
- Full CRM connector.
- Full sandbox container runtime.
- Public MCP adapter implementation.
- Full `page.tsx` rewrite before behavior is locked.
- Broad model-provider migration.

## Acceptance criteria

- `git rev-parse --show-toplevel` from PlotLot resolves to `/Users/earlperry/Desktop/Projects/EP/plotlot`.
- Current baseline is committed before feature implementation.
- Active branch is `feature/plotlot-workspace-harness` for implementation work.
- `.omx/plans/prd-plotlot-workspace-harness.md` and `.omx/plans/test-spec-plotlot-workspace-harness.md` exist.
- High-risk external writes from chat/tool paths are not executed without a governance decision.
- Evidence items include source type, tool name, retrieved timestamp, confidence, and workspace/project/site/run linkage where applicable.
- Runtime facade emits structured lifecycle/tool/evidence/approval events.
- Workspace/project/site route tests pass.
- Existing core unit tests and frontend lint/UI tests are run, with failures fixed or documented as pre-existing baseline failures.

## Release gates

- Backend unit tests for new runtime/governance/evidence/workspace code pass.
- Existing impacted backend unit tests pass.
- Frontend lint and UI tests pass for changed areas.
- At least one fixture-backed e2e path verifies the workspace shell.
- Security injection fixture proves external write is blocked or approval-gated.
- Architect verification approves final branch state.
