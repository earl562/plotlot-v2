---
url: https://alexzhang13.github.io/blog/2025/rlm/
status: reviewed
retrieved_at: 2026-05-04
---

# Alex Zhang — Recursive Language Models (RLMs)

## What it is

A blog post proposing **Recursive Language Models (RLMs)**: an inference pattern where a “root” LM interacts with an environment (e.g., a Python REPL) that holds the *full* prompt/context, and can spawn recursive LM calls to inspect subsets before producing the final answer.

## Key ideas worth copying

- **Context as a variable (not a prompt)**: store large context in an external environment; keep the root LM’s context lean.
- **REPL-mediated retrieval**: root LM uses code (regex/grep/filters) to narrow the search space, then calls child LM/RLM for targeted sub-queries.
- **Mitigating “context rot”** via decomposition + recursion instead of asking one model call to “carry everything”.
- **Modality-agnostic** in principle: if it can be loaded into memory/variables, the root LM can transform and query it.

## How it maps to PlotLot

- Treat zoning codes, GIS exports, long tool outputs, and past runs as **artifacts** stored outside the core chat context.
- Provide “REPL-like” affordances in the harness (server-side transforms, structured search over evidence) so the agent can narrow context *before* asking the model to reason.

## Source URLs

- https://alexzhang13.github.io/blog/2025/rlm/
