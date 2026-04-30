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

## Helper: extract arXiv URLs

From a single Obsidian note:

```bash
node .pi/skills/autoresearch/scripts/extract_arxiv_urls.mjs \
  --input "/Users/earlperry/Documents/AgenticHarnesses/Sandboxes/Harnesses/Harness info.md" \
  --output "docs/research/arxiv-urls.txt"
```

From an entire Obsidian vault directory:

```bash
node .pi/skills/autoresearch/scripts/extract_arxiv_urls_from_dir.mjs \
  --root "/Users/earlperry/Documents/AgenticHarnesses/Sandboxes" \
  --output "docs/research/arxiv-urls.txt"
```

## Helper: download PDFs + extract text

```bash
node .pi/skills/autoresearch/scripts/download_arxiv_papers.mjs \
  --input "docs/research/arxiv-urls.txt" \
  --out-dir "docs/research/_cache/arxiv" \
  --concurrency 2
```

Outputs (gitignored):
- `docs/research/_cache/arxiv/<id>.pdf`
- `docs/research/_cache/arxiv/<id>.txt`
- `docs/research/_cache/arxiv/index.json`

## Helper: fetch titles/abstracts/metadata (fast, no PDFs)

Preferred (arXiv export API):

```bash
node .pi/skills/autoresearch/scripts/fetch_arxiv_metadata.mjs \
  --input "docs/research/arxiv-urls.txt" \
  --output "docs/research/arxiv-abstracts.json" \
  --batch-size 20
```

Alternate (Jina abs-page extraction; may rate limit):

```bash
node .pi/skills/autoresearch/scripts/fetch_arxiv_abstracts.mjs \
  --input "docs/research/arxiv-urls.txt" \
  --output "docs/research/arxiv-abstracts.json" \
  --concurrency 2 --sleep-ms 500
```
