# Harness Backlog (PlotLot vertical)

This backlog turns reviewed research into shippable harness modules.

## P0 — Governance + auditability

- [x] Durable chat transcript + tool-call audit tables (`chat_messages`, `chat_tool_calls`).
- [x] Read APIs for transcript + tool calls.
- [x] Tool permission modes (deny-by-default external writes)
  - Implemented: `PLOTLOT_TOOL_PERMISSION_MODE=read_only|allow_writes`
  - Enforced at tool boundary + logged to tool-call audit trail.
  - TODO: interactive approvals (`ask_to_write`) for client UIs.
- [ ] Admission control / action governance (ACP-style)
  - deterministic rules keyed by tool+scope
  - cooldown/escalation on repeated denials/anomalies
- [ ] Prompt-injection filtering at input + tool-output boundary (SafeHarness L1)
  - scan ordinance chunks + web results for instruction injection
- [ ] Rollback/degradation strategy (SafeHarness L4)
  - fall back to safer mode on anomaly accumulation

## P0 — Evidence + provenance (trust-critical)

- [ ] Evidence ledger schema
  - citations to ordinance chunks (source_url, scraped_at, section)
  - parcel/provider provenance
- [ ] Output contracts require citations for key constraints
  - setbacks, max units, overlays, variances, etc.

## P1 — Memory + context engineering

- [ ] Semantic memory objects per property/project (facts + assumptions + confidence)
- [ ] Contradiction handling + staleness detection
- [ ] Compaction pipeline + reinjection of constraints (Claude Code/SemaClaw patterns)

## P1 — Orchestration

- [ ] SGH-style DAG execution for feasibility workflows
  - immutable plan versions
  - bounded recovery escalation
  - parallel specialist nodes (zoning/env/utilities/comps)

## P2 — Evaluation

- [ ] Red-team harness scenarios (AJAR/SafeHarness)
  - context poisoning, indirect injection, tool tampering, memory injection
- [ ] Vertical eval set + metric stack (memory survey)
  - effectiveness, memory quality, efficiency, governance
