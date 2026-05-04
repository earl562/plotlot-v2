---
url: https://blog.langchain.com/the-anatomy-of-an-agent-harness/
status: reviewed
retrieved_at: 2026-05-04
---

# LangChain — The Anatomy of an Agent Harness

## What it is

An article defining **Agent = Model + Harness** and breaking down what “harness engineering” means in practice.

## Key ideas worth copying

- **Definition**: the harness is everything that isn’t the model — prompts, tools/MCP schemas, sandboxes, orchestration, hooks/middleware.
- **Filesystem as foundational primitive** for durable state + collaboration surface.
- **Bash/code execution** as the default general-purpose tool (agents can synthesize ad-hoc tools via code).
- **Sandboxing + observability** (tests, logs, screenshots, traces) as the agent’s feedback loop.
- **Context management**: compaction/offloading + progressive disclosure of tools (skills) to reduce context rot.
- **Long-horizon execution** depends on durable state + verification loops more than raw model power.

## How it maps to PlotLot

- Reinforces our `docs/harness/README.md` modules: run ledger, evidence ledger, governance, memory, orchestration, eval.
- Suggests we should keep pushing “repo-owned artifacts” (skills/runbooks/evals) rather than encoding workflow in opaque controller code.

## Source URLs

- https://blog.langchain.com/the-anatomy-of-an-agent-harness/
- https://www.langchain.com/blog/the-anatomy-of-an-agent-harness
