---
repo: HKUDS/OpenHarness
url: https://github.com/HKUDS/OpenHarness
status: reviewed
---

# HKUDS/OpenHarness

## What it is

- Open-source **agent harness infrastructure** (“tool-use, skills, memory, multi-agent coordination”).
- Ships a CLI (`oh`) and a “personal agent” product example (`ohmo`) that can fork branches, run tests, open PRs, etc.
- Mentions a TUI stack (React+Ink) and supports multiple output modes (text/json/stream-json).

## Key patterns / primitives worth copying

- **Agent loop** capabilities called out explicitly:
  - streaming tool-call cycle
  - retries with exponential backoff
  - parallel tool execution
  - token counting + cost tracking
- **Harness toolkit**: file/shell/search/web/MCP tools + on-demand skill loading from Markdown.
- **Plugin ecosystem** concept: skills + hooks + agents.
- Treats harness as product surface (CLI/TUI), not just library code.

## How it maps to PlotLot

- Reference for how to present PlotLot as a **terminal-first harness**:
  - streaming event protocol
  - tool cards + rich rendering
  - durable session/workspace files
- Aligns with PlotLot primitives:
  - on-demand skills
  - multi-agent coordination
  - tool retry/cost accounting
- Use as a pattern library; PlotLot will still be verticalized around:
  - projects/sites/evidence/reports
  - connector governance
  - zoning/site-feasibility tools

## Risks / gotchas

- General-purpose harness; PlotLot still needs strict **evidence gating** + domain validators.
- Different stack (Python + Ink) vs our chosen stack (Node/TS + pi + FastAPI backend).

## Source URLs

- https://github.com/HKUDS/OpenHarness
