---
repo: bytedance/deer-flow
url: https://github.com/bytedance/deer-flow
status: reviewed
---

# bytedance/deer-flow

## What it is

- Open-source **“super agent harness”** (DeerFlow 2.0) that orchestrates **sub-agents**, **memory**, and **sandboxes**, powered by **extensible skills**.
- Explicitly designed for long-running, multi-step work with progressive skills + sandboxed execution.

## Key patterns / primitives worth copying

- **Skills as first-class modules** (Markdown workflows + references), with **progressive loading** (“only when the task needs them”).
- **Sub-agent orchestration**:
  - lead agent can spawn sub-agents with **scoped tools/context** and termination conditions
  - supports parallel work + structured handbacks + lead-agent synthesis.
- **Sandbox + filesystem**:
  - per-task execution environment w/ skills/workspace/uploads/outputs
  - multiple sandbox modes (local, Docker, Docker+Kubernetes/provisioner)
- **Context engineering**:
  - isolate sub-agent contexts
  - summarize/offload intermediate results to filesystem
  - compress completed steps to avoid context bloat
- **Long-term memory**:
  - persistent user/profile/preferences, stored locally (under user control)
  - avoids duplicate memory facts accumulation
- **Gateway + extensibility**: supports configurable MCP servers/skills; accepts skill archives with metadata.

## How it maps to PlotLot

- DeerFlow is a close reference for PlotLot’s target “consultant harness” UX/runtime:
  - PlotLot skills: zoning_research, site_selection, environmental_screening, utility_screening, outreach_ops, report_writer
  - PlotLot subagents: parcel, zoning, environmental, utility, market, evidence_reviewer
  - PlotLot sandbox modes: local vs Docker (and later k8s) for GIS joins, PDF parsing, artifact generation
  - PlotLot context strategy: isolate analysts; persist evidence+artifacts; summarize into workspace state
  - PlotLot memory: workspace/project/site/jurisdiction memory with dedupe + compaction

## Risks / gotchas

- DeerFlow is a general harness; PlotLot must keep **vertical constraints** (evidence ledger, “no claims without sources”, entitlement-specific guardrails).
- Progressive loading + many skills implies you need strong **skill discovery + routing** and good defaults.
- Sandbox complexity: Docker/K8s provisioner adds ops overhead; keep PlotLot’s sandbox MVP minimal first.

## Source URLs

- https://github.com/bytedance/deer-flow
- http://github.com/bytedance/deer-flow#-deerflow---20
- http://github.com/bytedance/deer-flow#official-website
- https://github.com/bytedance/deer-flow/blob/main/LICENSE
- https://github.com/bytedance/deer-flow/blob/main/Makefile
- https://github.com/bytedance/deer-flow/blob/main/README_fr.md
- https://github.com/bytedance/deer-flow/blob/main/README_ja.md
- https://github.com/bytedance/deer-flow/blob/main/README_ru.md
- https://github.com/bytedance/deer-flow/blob/main/README_zh.md
- https://github.com/bytedance/deer-flow/blob/main/backend/pyproject.toml
