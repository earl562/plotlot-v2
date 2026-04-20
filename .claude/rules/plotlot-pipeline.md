# PlotLot Pipeline Deep Dive

The analysis pipeline runs as a sequence of steps, each streamed to the frontend via SSE:

1. **Geocode** (`retrieval/geocode.py`) — Geocodio API → lat/lng, county, municipality, FIPS code
2. **Property Lookup** (`pipeline/lookup.py` + `property/`) — Routes to correct county ArcGIS API:
   - MDC: two-layer query (land use layer + zoning overlay layer)
   - Broward: parcel layer with zoning field
   - Palm Beach: spatial zoning query with geometry
   - Unknown counties: UniversalProvider (ArcGIS Hub discovery)
3. **Zoning Search** (`retrieval/search.py`) — pgvector hybrid search (RRF fusion of cosine similarity + BM25), limit=15 chunks
4. **LLM Extraction** (`retrieval/llm.py`) — Agentic LLM with tool calling extracts `NumericZoningParams`:
   - `max_density_units_per_acre` — e.g., 25.0 for RM-25
   - `min_lot_area_sqft` — minimum lot size per unit
   - `max_far` — floor area ratio
   - `max_lot_coverage_pct` — maximum lot coverage percentage
   - `max_height_ft` — maximum building height
   - `setback_front_ft`, `setback_side_ft`, `setback_rear_ft` — setback requirements
5. **Calculator** (`pipeline/calculator.py`) — Deterministic computation:
   - Applies 4 constraints: density, min_lot_area, FAR, buildable_envelope
   - Each constraint produces a max-units figure
   - Final result = `min(all constraints)` — the binding constraint
   - Returns `DensityAnalysis` with per-constraint breakdown
6. **Comparable Sales** (`pipeline/comps.py`) — ArcGIS Hub sales data within 3-mile radius
7. **Pro Forma** (`pipeline/proforma.py`) — Residual land valuation (GDV - costs - margin)
