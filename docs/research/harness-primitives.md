# Harness primitives (consolidated)

A running, paper-backed list of harness/agent engineering primitives we can reuse for PlotLot’s land-use / site-feasibility agents.

## Primitives index

- Signature-driven initialization / playbooks (error-class routing)
- Interactive state introspection (runtime queries, not just static context)
- Deterministic replay / time-travel debugging
- Context compaction + sandboxed distillation scripts
- Closed-loop patching/validation (verify → feed failures back)
- Deterministic output/patch correction (auto-fix formatting/structure)
- Tool abstraction + command validation (guardrails)

---

## DebugHarness (2604.03610v1)

- **Signature-driven initialization**: parse incident/crash signature → inject type-specific troubleshooting heuristics + “rules of engagement”.
- **Interactive state introspection**: live debugger/tool control (GDB/pwndbg) + deterministic replay (rr) to test hypotheses against real runtime state.
- **Static↔dynamic bridge**: LSP/clangd mapping from runtime frames/symbols → source locations/snippets.
- **Context compaction**: summarize verbose tool outputs; allow sandboxed scripts over raw outputs to extract signal.
- **Closed-loop validation**: patch → rebuild → rerun PoC + tests; distill failures back into context.
- **Deterministic patch correction**: auto-repair malformed diffs to reduce wasted iterations.
- **Tool abstraction + guardrails**: MCP (JSON-RPC) + command validation layers.
