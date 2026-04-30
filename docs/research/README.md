# Research

Repo-owned research used to inform PlotLot's agentic harness architecture.

## arXiv registry

- `arxiv-urls.txt` is a deduplicated list of arXiv links extracted from the Obsidian research notes.
- Use `.pi/skills/autoresearch/scripts/extract_arxiv_urls.mjs` to refresh the list.

## Workflow

1. Refresh URL inventories (Obsidian → repo).
2. Summarize sources into `docs/research/autoresearch/<slug>.md`.
3. Convert summaries into:
   - runbooks/skills (`.pi/skills/`)
   - harness specs (`docs/prd/`, `docs/architecture/`)
   - eval cases (`plotlot/tests/eval/`)
