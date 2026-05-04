---
url: https://blog.langchain.com/deep-agents-v0-5/
status: reviewed
retrieved_at: 2026-05-04
---

# LangChain — Deep Agents v0.5

## What it is

A release post describing updates to `deepagents` / `deepagentsjs` focused on making long-running, multi-agent work less blocking.

## Key ideas worth copying

- **Async subagents**: background subagents that return immediately with a task ID rather than blocking the supervisor loop.
- **Motivation**: as tasks stretch from seconds to minutes, blocking delegation becomes a bottleneck.
- Mentions expanded multimodal filesystem support (agent can reason over non-text artifacts).

## How it maps to PlotLot

- We should treat “long zoning runs” (Municode crawl, GIS layer discovery, parcel enrichment) as **background tasks** with durable progress + resumability.
- Our harness should expose **task IDs + progress events** to the web client rather than freezing the chat loop.

## Source URLs

- https://blog.langchain.com/deep-agents-v0-5/
- https://www.langchain.com/blog/deep-agents-v0-5
