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

## Query profiles + Paperclip-style search

- `arxiv-search-profiles/harness-agents.json` — default topic profile for harness engineering / long-horizon / terminal / multi-agent discovery.
- `scripts/search_harness_arxiv.mjs` — searches both:
  - the existing arXiv corpus already extracted from the Obsidian vault
  - new remote arXiv candidates not yet in the vault
- Output artifacts:
  - `arxiv-harness-search.json`
  - `arxiv-harness-search.md`
  - `arxiv-discovery-candidates.txt`

Example:

```bash
node scripts/search_harness_arxiv.mjs
node scripts/search_harness_arxiv.mjs --query "context engineering agents" --query "tool-using coding agents"
node scripts/search_harness_arxiv.mjs --vault-report "$HOME/Documents/AgenticHarnesses/Sandboxes/Harnesses/Harness Engineering KG/ArXiv Search - Harness Agents.md"
```

Note: this is intentionally **Paperclip-style**, not a direct Paperclip integration. Paperclip currently targets biomedical corpora (bioRxiv / medRxiv / PMC), while this repo needs arXiv CS papers.

## Workflow

1. Refresh URL inventories (Obsidian → repo).
2. For arXiv: fetch metadata → download PDFs → extract text → generate note stubs.
3. Run topic search/discovery over the local + remote arXiv corpus.
4. Summarize sources into `docs/research/autoresearch/<slug>.md` or into `docs/research/arxiv-notes/<id>.md`.
5. Convert summaries into:
   - runbooks/skills (`.pi/skills/`)
   - harness specs (`docs/prd/`, `docs/architecture/`)
   - eval cases (`plotlot/tests/eval/`)
