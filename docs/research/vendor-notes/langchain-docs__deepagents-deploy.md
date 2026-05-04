---
url: https://docs.langchain.com/oss/python/deepagents/deploy#subagents
status: reviewed
retrieved_at: 2026-05-04
---

# LangChain Docs — Deep Agents deploy (memory + subagents)

## What it is

Documentation describing Deep Agents’ deployment model, including **per-user memory** and **subagent isolation**.

## Key ideas worth copying

- **Per-user writable memory** seeded from a template (`user/AGENTS.md`); persisted across conversations.
- **Memory namespaces**:
  - shared assistant memory is read-only to users
  - user memory is per-user writable
  - subagents get isolated namespaces under `/memories/subagents/<name>/`
- **Subagents**:
  - each subagent has its own system prompt and optional skills/tools
  - configuration is filesystem-native (directory structure + TOML + AGENTS.md)

## How it maps to PlotLot

- Matches our goal of **workspace-native durability**:
  - workspace/project/site-specific memory should be explicit and inspectable
  - child-agent/tool contexts must be isolatable to prevent cross-contamination

## Source URLs

- https://docs.langchain.com/oss/python/deepagents/deploy#subagents
