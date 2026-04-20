---
name: plotlot-pipeline
description: PlotLot analysis pipeline architecture, error taxonomy, and retry strategies
user-invocable: false
---

# PlotLot Analysis Pipeline

## 6-Step Pipeline Architecture

```
Address → Geocode → Property Lookup → Zoning Search → LLM Extraction → Density Calculator
```

### Step 1: Geocode (`retrieval/geocode.py`)
- Geocodio API → lat/lng, county, municipality, FIPS code, state
- Passes state param downstream for Hub discovery

### Step 2: Property Lookup (`pipeline/lookup.py` + `property/`)
- Registry routes to correct provider (MDC, Broward, Palm Beach, Mecklenburg)
- Unknown counties fall back to UniversalProvider (ArcGIS Hub discovery)
- Returns PropertyRecord with folio, lot_size, zoning_code, geometry

### Step 3: Zoning Search (`retrieval/search.py`)
- pgvector hybrid search: cosine similarity + BM25 (RRF fusion)
- Returns top 15 zoning ordinance chunks for the municipality

### Step 4: LLM Extraction (`retrieval/llm.py`)
- Agentic LLM with tool calling extracts NumericZoningParams
- Fallback chain: Claude Sonnet → Gemini Flash → NVIDIA Llama → Kimi K2.5
- Per-model circuit breakers (3 failures in 5min → switch)

### Step 5: Density Calculator (`pipeline/calculator.py`)
- 4 constraints: density, min_lot_area, FAR, buildable_envelope
- Final result = min(all constraints) — the binding constraint
- Returns DensityAnalysis with per-constraint breakdown

### Step 6: SSE Streaming (`api/routes.py`)
- Events: geocode, property, zoning, analysis, calculator, heartbeat, error, done
- Heartbeat every 15s for Render's 30s proxy timeout

## Error Taxonomy

| Error | Source | Retry? |
|-------|--------|--------|
| GeocodingError | Geocodio API | Yes (3x exponential) |
| PropertyLookupError | ArcGIS API | Yes (3x exponential) |
| ZoningSearchError | pgvector | No (database issue) |
| LLMExtractionError | LLM API | Yes (circuit breaker) |
| CalculatorError | Calculator | No (logic error) |

## Retry Strategies

- Network-bound steps: exponential backoff (1s, 2s, 4s)
- LLM calls: circuit breaker pattern (trip after 3 failures in 5min)
- ArcGIS calls: 30s timeout, 3 retries
