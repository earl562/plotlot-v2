# Research

Repo-owned research used to inform PlotLot's agentic harness architecture.

## arXiv registry

- `arxiv-urls.txt` — arXiv links extracted from the Obsidian research notes.
- `arxiv-abstracts.json` — arXiv export-API metadata (title/abstract/authors/categories).
- `arxiv-topic-map.md` — coarse topic clustering based on title/abstract regex.
- `arxiv-notes/` — per-paper note stubs (abstract + placeholders).
- `arxiv-abstracts.md` — rendered abstracts for quick browsing.

Refresh via scripts in `.pi/skills/autoresearch/scripts/`.

## Workflow

1. Refresh URL inventories (Obsidian → repo).
2. Summarize sources into `docs/research/autoresearch/<slug>.md`.
3. Convert summaries into:
   - runbooks/skills (`.pi/skills/`)
   - harness specs (`docs/prd/`, `docs/architecture/`)
   - eval cases (`plotlot/tests/eval/`)
