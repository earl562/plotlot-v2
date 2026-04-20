# PlotLot Ingestion Pipeline

The ingestion pipeline (`pipeline/ingest.py`) processes a municipality's zoning ordinances:

1. **Discovery** — Query Municode API to find the municipality's code library
2. **Scrape** — Download all zoning-related sections (Title/Chapter filtering)
3. **Chunk** — Split into ~500-token chunks with overlap, preserving section headers
4. **Embed** — NVIDIA NIM embeddings (1024d vectors)
5. **Store** — Upsert into pgvector with metadata (municipality, section, chapter)

Currently ingested municipalities and chunk counts:
| Municipality | Chunks | County |
|-------------|--------|--------|
| Miami Gardens | 3,561 | Miami-Dade |
| Miami-Dade County | 2,666 | Miami-Dade |
| Boca Raton | 1,538 | Palm Beach |
| Miramar | 241 | Broward |
| Fort Lauderdale | 136 | Broward |

88 municipalities are discoverable on Municode. West Palm Beach uses enCodePlus (not supported yet).
