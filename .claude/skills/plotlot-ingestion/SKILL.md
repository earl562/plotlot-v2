---
name: plotlot-ingestion
description: PlotLot ingestion pipeline — Municode discovery, scraping, chunking, embedding
user-invocable: false
---

# PlotLot Ingestion Pipeline

## Pipeline Steps (`pipeline/ingest.py`)

1. **Discovery** — Query Municode API to find municipality's code library
2. **Scrape** — Download zoning-related sections (Title/Chapter filtering)
3. **Chunk** — Split into ~500-token chunks with overlap, preserving section headers
4. **Embed** — NVIDIA NIM embeddings (1024d vectors)
5. **Store** — Upsert into pgvector with metadata (municipality, section, chapter)

## Currently Ingested
| Municipality | Chunks |
|-------------|--------|
| Miami Gardens | 3,561 |
| Miami-Dade County | 2,666 |
| Boca Raton | 1,538 |
| Miramar | 241 |
| Fort Lauderdale | 136 |

## Municode Discovery
- 88 municipalities discoverable via Municode API
- West Palm Beach uses enCodePlus (not supported)
- Auto-discovery finds zoning titles/chapters

## CLI Commands
```bash
# List discoverable municipalities
uv run plotlot-search --list-municipalities

# Ingest a municipality
uv run plotlot-ingest --municipality "City Name"

# Verify search quality
uv run plotlot-search --municipality "Name" --query "residential density" --limit 5
```
