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

### URL registries

- `docs/research/obsidian-urls.txt` / `docs/research/obsidian-urls.json`
- `docs/research/obsidian-url-map.md`

### arXiv corpus

- `docs/research/arxiv-urls.txt`
- `docs/research/arxiv-abstracts.json`
- `docs/research/arxiv-topic-map.md`
- `docs/research/arxiv-abstracts.md`
- `docs/research/arxiv-notes/` (per-paper note stubs)
- `docs/research/arxiv-notes-status.md` (reviewed vs stub)

### GitHub corpus

- `docs/research/github-repos.txt` / `docs/research/github-repos.json`
- `docs/research/github-notes/` (per-repo note stubs)
- `docs/research/github-notes-status.md`

### Freeform research notes

- `docs/research/autoresearch/<slug>.md`

## Helper: extract all URLs from Obsidian vault

```bash
node .pi/skills/autoresearch/scripts/extract_urls_with_sources.mjs \
  --root "/Users/earlperry/Documents/AgenticHarnesses/Sandboxes" \
  --output-json "docs/research/obsidian-urls.json" \
  --output-txt "docs/research/obsidian-urls.txt"

node .pi/skills/autoresearch/scripts/categorize_urls.mjs \
  --input "docs/research/obsidian-urls.json" \
  --output "docs/research/obsidian-url-map.md"
```

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

## Helper: download full PDFs + extract text (required for “full paper” review)

```bash
node .pi/skills/autoresearch/scripts/download_arxiv_papers.mjs \
  --input "docs/research/arxiv-urls.txt" \
  --out-dir "docs/research/_cache/arxiv" \
  --concurrency 2
```

Notes:
- This downloads the **full PDF** for each arXiv ID and runs `pdftotext` to produce `docs/research/_cache/arxiv/<id>.txt`.
- The `_cache/` directory is gitignored; commit only the derived, human-reviewed summaries/notes.

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

## Helper: build arXiv browsing artifacts

```bash
node .pi/skills/autoresearch/scripts/build_arxiv_topic_map.mjs \
  --input docs/research/arxiv-abstracts.json \
  --output docs/research/arxiv-topic-map.md

node .pi/skills/autoresearch/scripts/render_arxiv_abstracts_md.mjs \
  --input docs/research/arxiv-abstracts.json \
  --output docs/research/arxiv-abstracts.md

node .pi/skills/autoresearch/scripts/generate_arxiv_note_stubs.mjs \
  --input docs/research/arxiv-abstracts.json \
  --out-dir docs/research/arxiv-notes

node .pi/skills/autoresearch/scripts/list_unreviewed_notes.mjs \
  --notes-dir docs/research/arxiv-notes \
  --output docs/research/arxiv-notes-status.md
```

## Helper: extract GitHub repos + generate notes

```bash
node .pi/skills/autoresearch/scripts/extract_github_repos.mjs \
  --input docs/research/obsidian-urls.json \
  --output-json docs/research/github-repos.json \
  --output-txt docs/research/github-repos.txt

node .pi/skills/autoresearch/scripts/generate_github_note_stubs.mjs \
  --input docs/research/github-repos.json \
  --out-dir docs/research/github-notes

node .pi/skills/autoresearch/scripts/list_github_notes.mjs \
  --notes-dir docs/research/github-notes \
  --output docs/research/github-notes-status.md
```
