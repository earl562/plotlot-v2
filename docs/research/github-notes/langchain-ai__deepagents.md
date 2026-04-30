---
repo: langchain-ai/deepagents
url: https://github.com/langchain-ai/deepagents
status: reviewed
---

# langchain-ai/deepagents

## What it is

- LangChain OSS project: an **opinionated, batteries-included agent harness** with a ready-to-run agent, plus a CLI “coding agent in your terminal”.

## Key patterns / primitives worth copying

- Treat “agent = model + harness” as productized defaults:
  - **planning** (`write_todos`)
  - **filesystem tools** (read/write/edit/ls/glob/grep)
  - **shell tool** (execute, with sandboxing)
  - **sub-agent tool** (`task`) for delegation with isolated contexts
  - **context management** (auto-summarization; large outputs saved to files)
- Clear separation between:
  - core harness (tools + prompt defaults)
  - customization points (swap model, add tools, change system prompt)
- Explicit support for MCP via adapters.

## How it maps to PlotLot

- PlotLot’s CLI/TUI can mirror the same “batteries included” feel, but with vertical tools:
  - planning: risk register + open questions + next steps
  - filesystem: project artifacts, evidence exports, report drafts
  - subagents: zoning/environment/utilities analysts
  - context mgmt: compaction into structured workspace state
- Use DeepAgents as a reference for:
  - minimal default toolset
  - subagent isolation
  - automatic compaction policies

## Risks / gotchas

- DeepAgents is general-purpose; PlotLot needs stronger **evidence + governance** constraints than a generic coding agent.
- LangChain ecosystem adds dependency surface area; copy patterns even if we don’t adopt the full stack.

## Source URLs

- https://github.com/langchain-ai/deepagents
