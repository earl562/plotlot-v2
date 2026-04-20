---
name: plotlot-chat
description: PlotLot agentic chat system — 10 tools, dynamic masking, session memory
user-invocable: false
---

# PlotLot Chat System

## Architecture (`api/chat.py`)
Agentic chat with conversational property research capabilities.

## 10 Tools
1. `geocode` — Address to lat/lng via Geocodio
2. `lookup_property_info` — ArcGIS property data
3. `search_zoning_ordinance` — pgvector hybrid search
4. `web_search` — General web search
5. `property_search` — Search properties by criteria
6. `filter` — Filter/sort results
7. `dataset_info` — Database statistics
8. `export` — Export results
9. `spreadsheet` — Google Sheets integration
10. `document_creation` — Generate reports

## Dynamic Tool Masking
Tools are masked/unmasked based on conversation state:
- Start: only `geocode` available
- After geocode: `lookup_property_info` unlocked
- After lookup: `search_zoning_ordinance` unlocked
- All tools available after core workflow complete

## Session Memory
- LRU cache: 100 sessions max
- 1hr TTL per session
- Geocode cache: session-level lat/lng for consistent precision
- Token budget: 50K tokens per session
