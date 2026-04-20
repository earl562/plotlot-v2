---
name: plotlot-arcgis
description: ArcGIS Hub discovery, county schemas, field mapping for PlotLot
user-invocable: false
---

# PlotLot ArcGIS Integration

## Hub Discovery (`property/hub_discovery.py`)
- Queries `hub.arcgis.com/api/v3/datasets` — public, no auth needed
- Search: "parcels {county} {state}" and "zoning {county} {state}"
- Scores datasets by field keyword matching (FOLIO, PARCEL, ZONE, etc.)
- Returns (parcels_dataset, zoning_dataset) or None

## County ArcGIS Schemas

### Miami-Dade (Two-Layer)
- Land use layer + zoning overlay layer
- Fields: FOLIO, TRUE_SITE_ADDR, ASMNT_YR, BLDG_CNT

### Broward
- BCPA MapServer, parcel layer with inline zoning field
- Fields: FOLIO, SITEADDR, ZONING, LOT_SIZE

### Palm Beach
- Spatial zoning query on dedicated layer
- Fields: PCN, SITUS_ADDR, ZONE_CODE, ACREAGE

### Mecklenburg (NC)
- Charlotte GIS MapServer
- Fields: PID, SITE_ADDR, ZONE_CLASS, LAND_USE_CD, BLDG_SQFT

## Field Mapping (`property/field_mapper.py`)
- Phase 1: Heuristic keyword matching (24 PropertyRecord fields x curated keywords)
- Phase 2: LLM fallback if confidence < 0.7 (maps remaining unmapped fields)
- Auto unit conversion: ACRES -> sqft (x43,560), SQ_M -> sqft (x10.764)

## UniversalProvider (`property/universal.py`)
4-step flow:
1. Cache lookup (Firestore, 7-day TTL)
2. Hub discovery (if not cached)
3. Parcel query (address match -> spatial fallback)
4. Zoning query (spatial on zoning dataset)

## ArcGIS REST Utilities (`property/arcgis_utils.py`)
- `query_arcgis(url, where, out_fields)` — WHERE clause query
- `spatial_query(url, lat, lng)` — point-in-polygon
- `normalize_address(address)` — strip city/state, uppercase
- `extract_parcel_rings(feature)` — polygon geometry extraction
