---
repo: anomalyco/opencode
url: https://github.com/anomalyco/opencode
status: stub
retrieved_at: 2026-05-04
---

# anomalyco/opencode

## What it is

- An open-source AI coding agent with a strong **TUI-first** posture.

## Notable primitives

- **Multi-agent / persona split**:
  - a “build” agent (full access)
  - a “plan” agent (read-only; denies edits; asks permission before bash)
- **Provider-agnostic** stance (not tied to a single model provider).
- Mentions a **client/server architecture** so the UI is just one client.

## How it maps to PlotLot

- Strong design reference for:
  - permission modes (read-only vs allow writes)
  - making the harness legible via explicit modes/roles
  - treating TUI/web as clients over a durable backend “system of record”

## Source URLs

- https://github.com/anomalyco/opencode
