---
repo: mindfold-ai/Trellis
url: https://github.com/mindfold-ai/Trellis
status: reviewed
---

# mindfold-ai/Trellis

## What it is

- A **team AI coding harness** that turns a monolithic agent instruction file (e.g. `CLAUDE.md`) into a **progressive, repo-owned wiki** of specs/tasks/workflows/journals that agents load only when needed.
- Installs a `.trellis/` directory and generates platform-specific adapters for Claude Code, Cursor, Codex, OpenCode, Pi Agent, etc.

## Key patterns / primitives worth copying

- **Progressive disclosure** of repo knowledge:
  - avoid stuffing giant prompts; load relevant docs at the right time.
- Clear repo-owned layers:
  - `.trellis/spec/` (team standards)
  - `.trellis/tasks/` (PRDs + acceptance)
  - `.trellis/workspace/` (session journals/handoffs)
  - `.trellis/workflow.md` (shared lifecycle)
- **Platform adapters**: same source-of-truth docs, different agent shells.
- Emphasis on **task → spec → build → check → learn** loops.

## How it maps to PlotLot

- PlotLot should adopt the same *shape* but for land-use/site-feasibility:
  - `docs/architecture/` (harness/runtime boundaries)
  - `docs/prd/` + `docs/plans/` (task PRDs + acceptance)
  - `docs/runbooks/` (zoning research, site screening, outreach)
  - `docs/research/` (source registry + summaries)
  - skills in `.pi/skills/` (executable runbooks)
- Use this to make PlotLot’s harness:
  - **repo-owned**
  - **reviewable**
  - **portable across models/gateways**

## Risks / gotchas

- Trellis is **AGPL-3.0**; copy patterns, not code, unless you’re OK with AGPL constraints.
- Coding-harness abstractions need vertical translation:
  - PlotLot “tasks” are projects/sites/evidence/reports, not PRs.

## Source URLs

- https://github.com/mindfold-ai/Trellis
- http://github.com/mindfold-ai/Trellis#start-of-content
