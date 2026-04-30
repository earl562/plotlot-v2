---
name: autoresearch
description: Research skill for collecting, deduplicating, and summarizing URLs/papers into repo-owned notes. Use to ingest arXiv URLs, extract key primitives, and write structured summaries.
---

# Autoresearch (dev-only)

Repo-owned research workflow inspired by open-source "autoresearch".

## Rules

- Prefer primary sources.
- Keep outputs structured + actionable.
- Write results into repo docs for review.

## Outputs

- `docs/research/arxiv-urls.txt` (deduped URL list)
- `docs/research/autoresearch/<slug>.md` (summaries)

## Helper: extract arXiv URLs from Obsidian note

```bash
node .pi/skills/autoresearch/scripts/extract_arxiv_urls.mjs \
  --input "/Users/earlperry/Documents/AgenticHarnesses/Sandboxes/Harnesses/Harness info.md" \
  --output "docs/research/arxiv-urls.txt"
```
