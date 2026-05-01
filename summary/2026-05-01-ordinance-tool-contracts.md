# 2026-05-01 — Ordinance tool contracts (canonical ports + citations)

Branch: `codex/dev-branch-pipeline`  
Delivery commit: `180dade` (“Unify ordinance tool contracts and improve local citations”)

## Why this was needed

The harness docs + gold fixtures describe ordinance retrieval via:

- `search_ordinances`
- `fetch_ordinance_section`

…but the harness runtime only exposed `search_zoning_ordinance` and the hybrid search results did
not consistently carry provenance fields needed for citations.

## What changed

- Added canonical read-only ordinance tools:
  - `search_ordinances` (returns `OrdinanceSearchResult` shape)
  - `fetch_ordinance_section` (returns a single cited chunk)
- Upgraded hybrid search to return provenance fields (where present in DB):
  - `chapter`, `municode_node_id`, `source_url` (and `chunk_id`)
- Updated PRD + test spec + architecture doc sketches to match the implemented tool-gateway
  pattern:
  - `POST /api/v1/tools/call`
  - `POST /api/v1/mcp/tools/call`

## Verification

See `summary/2026-05-01-verification.md` (ruff + unit + frontend lanes).

