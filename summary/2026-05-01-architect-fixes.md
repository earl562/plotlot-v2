# 2026-05-01 — Architect review follow-ups (harness governance + spec alignment)

Branch: `codex/dev-branch-pipeline`  
Delivery commit: `c221e4c` (“Harden harness governance and align docs with implementation”)

## Why this was needed

An architect review flagged drift between:

- what the docs/specs claimed (tool names + routes),
- what the tool registry exposed,
- what the harness runtime could actually execute (handlers),
- and what governance controls (e.g., `live_network_allowed`) were supposed to enforce.

## What changed

### Harness runtime safety + implementability

- **No approvals for unimplemented tools**: the runtime now checks handler availability before returning `pending_approval`.
- **Redacted tool-call events**: emitted events include `arg_keys` (not full argument values) to reduce risk of accidental secret leakage.
- Exposed `has_handler()` so adapters can filter tool listings.

### Tool listing surfaces

- `/api/v1/tools` (REST) and `/api/v1/mcp/tools/list` (MCP-over-HTTP) now **only list tools that have registered handlers** in the default runtime.

### Governance: enforce live-network gating

- `ToolPolicy` now enforces `live_network_allowed` for:
  - `EXPENSIVE_READ`
  - `WRITE_EXTERNAL`
  - `EXECUTION`

This keeps deterministic/no-auth lanes fail-closed by default.

### Default runtime correctness

- Evidence no longer uses `project_id="prj_unknown"` fallbacks; it uses a deterministic UUID5 default project id when missing.
- Removed hard-coded Florida defaults:
  - Municode live search derives state from config (or optional tool arg).
  - Open-data discovery requires explicit `state`.

### Docs/spec alignment

- Updated architecture header metadata to match the branch.
- Updated executive summary examples to match current tool names + actual HTTP routes (`/api/v1/tools/call`, `/api/v1/mcp/tools/call`).

## Verification

See `summary/2026-05-01-verification.md` (Ruff + unit tests + frontend lint/tsc/vitest/build).

