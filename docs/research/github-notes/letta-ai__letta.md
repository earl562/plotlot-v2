---
repo: letta-ai/letta
url: https://github.com/letta-ai/letta
status: reviewed
---

# letta-ai/letta

## What it is

- Letta (formerly MemGPT): platform for **stateful agents with advanced memory**.
- Offers:
  - a local terminal product (“Letta Code” CLI)
  - a hosted **Agents API** + TS/Python SDKs
- Supports **skills** and **subagents**; positions itself as **model-agnostic**.

## Key patterns / primitives worth copying

- **Explicit memory blocks** as a first-class configuration surface (persona/human/org/project, etc.).
- Clear separation between:
  - runtime agent loop
  - persistent memory representation
  - tools
- Model portability emphasis (swap models while preserving agent state).

## How it maps to PlotLot

- PlotLot should implement “memory blocks” (app-owned) for:
  - user preferences
  - org underwriting rules
  - project criteria
  - site-specific findings
  - jurisdiction quirks
- Use Letta as a reference for:
  - durable memory abstractions
  - memory editing workflows (dedupe, consolidation)
  - subagent interfaces

## Risks / gotchas

- If you used Letta’s hosted API as the memory store, you risk the lock-in issue noted in your research: **provider-owned state** becomes expensive to migrate.
- PlotLot should keep memory in Postgres (plus vector) and treat external agent platforms as optional adapters.

## Source URLs

- https://github.com/letta-ai/letta
