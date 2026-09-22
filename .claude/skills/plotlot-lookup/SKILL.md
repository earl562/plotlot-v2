---
name: plotlot-lookup
description: Run PlotLot's canonical address lookup with evidence-first zoning retrieval and honest coverage states.
user-invocable: true
---

# PlotLot Reliable Lookup

Use this skill when the user asks what can be built at a property, wants zoning facts for an address, or needs a parcel/zoning lookup before deeper underwriting.

## Canonical flow

1. Call the PlotLot lookup/full-analysis capability for the address.
2. Treat county/parcel facts and indexed ordinance evidence as separate evidence tracks.
3. If an exact zoning district is known, pass it back into zoning search as the `zone_code` so retrieval stays pinned to that district.
4. Present verified facts first: parcel identity, municipality/county, zoning district, lot size, source-backed dimensional standards.
5. If dimensional standards are missing, say they are missing. Do not infer them from general knowledge.
6. Only present max units/buildability when deterministic calculator inputs are available.
7. Use deeper chat, comps, pro forma, or outreach only after the lookup result is established.

## Reliability contract

- Address resolution failure: stop and ask for a corrected address.
- Property record found but ordinance coverage missing: return zoning-only coverage and offer ingestion.
- Retrieval returns conflicting evidence: surface the conflict; do not pick a convenient value.
- Model/provider failure: preserve deterministic parcel/zoning facts and return a partial result rather than inventing values.
- Sources and confidence are part of the product output, not optional decoration.

## Integration surfaces

The same lookup behavior should back the web Lookup screen, REST analysis endpoint, MCP tools, and future ChatGPT/plugin actions. Do not duplicate zoning logic in adapters.
