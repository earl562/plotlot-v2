# PlotLot Lookup Rollout

The first product goal is simple: **address in -> reliable, source-backed lookup out**.

## Product contract

Lookup must answer, in order:

1. Did we resolve the right parcel?
2. What jurisdiction governs it?
3. What zoning district does the official property/GIS source report?
4. Do we have indexed ordinance evidence for that district?
5. Which dimensional standards are explicitly supported?
6. What can the deterministic calculator compute from those supported inputs?
7. What remains unknown?

A lookup is allowed to be partial. It is not allowed to look complete when critical evidence is missing.

## Runtime priorities

### 1. Deterministic facts first

Geocoding, parcel identity, municipality, county, zoning code, lot size, and calculator math do not require an LLM. Preserve those facts even when model inference fails.

### 2. Retrieval before generation

The LLM interprets retrieved ordinance evidence. It does not replace retrieval. Exact district metadata is passed separately from the semantic query so natural-language intent cannot wash out the parcel's zoning code.

### 3. OpenRouter free for development reliability

When `OPENROUTER_API_KEY` is configured and `OPENROUTER_PREFERRED=true`, PlotLot tries `openrouter/free` first, then falls back to the existing primary provider and Groq. The model is configurable with `OPENROUTER_MODEL`.

This path is for low-cost development and reliability testing, not a contractual production SLA.

### 4. Cleaner ingestion

Duplicate normalized ordinance chunks are removed before embedding. This reduces wasted embedding calls and prevents duplicate chunks from crowding distinct evidence out of retrieval results.

## Phase gates

### Phase A - address/parcel

Pass when the resolved address, county, municipality, parcel identifier and zoning code match the official provider for a small launch set.

### Phase B - ingestion

Pass when scraped sections produce non-empty chunks, duplicate rate is visible, embeddings validate, and stored chunk counts are stable across idempotent reruns.

### Phase C - retrieval

Pass when exact-zone queries surface district-specific sections for uses, density, setbacks, height/FAR/coverage and parking. Fail when generic provisions outrank the parcel district.

### Phase D - interpretation

Pass when the model returns only values supported by retrieved chunks and degrades to null/unknown when evidence is absent.

### Phase E - product lookup

Pass when a user can enter an address and understand parcel facts, zoning evidence, buildability, confidence and what is missing without opening chat.

## Integration rollout

- **Web:** QuickLookup is the primary user workflow.
- **REST:** `/api/v1/analyze` and streaming analysis remain the canonical transport API.
- **MCP:** `run_full_analysis` and `search_zoning(..., zone_code=...)` expose the same lookup/retrieval contract to external agents.
- **Skills:** `.claude/skills/plotlot-lookup/SKILL.md` tells coding/agent clients how to use the canonical capabilities without inventing facts.
- **Plugin / connector surface:** future adapters should call REST/MCP contracts rather than reimplement zoning, retrieval or calculator logic.

## UX story

The Lookup screen should communicate the actual workflow:

**Resolve parcel -> verify zoning evidence -> calculate buildability**

Do not lead with comps, pro forma, or broad "AI analysis" claims. Those are follow-on workflows after the user trusts the lookup.
