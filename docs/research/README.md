# Research

Repo-owned research used to inform PlotLot's agentic harness architecture.

## arXiv registry

- `arxiv-urls.txt` — arXiv links extracted from the Obsidian research notes.
- `arxiv-abstracts.json` — arXiv export-API metadata (title/abstract/authors/categories).
- `arxiv-topic-map.md` — coarse topic clustering based on title/abstract regex.
- `arxiv-notes/` — per-paper note stubs (abstract + placeholders).
- `arxiv-abstracts.md` — rendered abstracts for quick browsing.

Refresh via scripts in `.pi/skills/autoresearch/scripts/`.

## Obsidian URL registry

- `obsidian-urls.txt` / `obsidian-urls.json` — all URLs extracted from the Obsidian vault snapshot (with source files).
- `obsidian-url-map.md` — categorized URL map + counts.

## Workflow

1. Refresh URL inventories (Obsidian → repo).
2. For arXiv: fetch metadata → download PDFs → extract text → generate note stubs.
3. Summarize sources into `docs/research/autoresearch/<slug>.md` or into `docs/research/arxiv-notes/<id>.md`.
4. Convert summaries into:
   - runbooks/skills (`.pi/skills/`)
   - harness specs (`docs/prd/`, `docs/architecture/`)
   - eval cases (`plotlot/tests/eval/`)
