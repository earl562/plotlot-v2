---
url: https://openai.com/index/harness-engineering/
status: reviewed
retrieved_at: 2026-05-04
---

# OpenAI — Harness engineering (Codex)

## What it is

OpenAI write-up describing *harness engineering* as the work of turning a raw model into a reliable, legible, high-throughput engineering system via repo-owned artifacts, guardrails, and feedback loops.

## Key ideas worth copying

- **Repository as the system of record**: keep operational knowledge (runbooks, plans, reliability rules, etc.) versioned in-repo so future runs can deterministically reload it.
- **Legibility over cleverness**: optimize for outputs that are easy for *future agents* (and humans) to audit, replay, and modify.
- **Encode taste & constraints into tooling**: enforce invariants with linters / structural tests; write error messages that include remediation instructions so failures become *context injection*.
- **Throughput changes workflow economics**: when agents can generate changes quickly, short-lived PRs + rapid iteration beats heavyweight upfront process.

## How it maps to PlotLot

- Strengthens our direction in `docs/harness/README.md`:
  - run/event ledger + evidence ledger + governance middleware + memory + evaluation.
- Matches the “repo-owned runbooks/skills” pattern we’re adopting for workspace-native, repeatable zoning/site-feasibility workflows.

## Source URLs

- https://openai.com/index/harness-engineering/
