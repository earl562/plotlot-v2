# OpenData / ArcGIS / Socrata Connector Contract

## Purpose

Provide normalized parcel/zoning/permit/infrastructure facts from public ArcGIS FeatureServer/MapServer and Socrata/Tyler SODA sources. Avoid mirroring entire datasets while still storing evidence, cache, lineage, and freshness metadata for claims used in reports.

## Tool contracts (conceptual)

- `discover_open_data_layers(county/state, lat/lng) -> [LayerCandidate]`
- `query_property_layer(selector) -> FeatureQueryResult`

## Evidence requirements

Every open-data claim used in a report must include:

- service URL (FeatureServer/MapServer or SODA endpoint)
- dataset or layer identifier
- query parameters/URL
- retrieved timestamp
- license/terms URL when available
- publisher/source when available
- raw source hash / content hash
- field mapping confidence

## Governance

- discovery/query are `READ_ONLY` or `EXPENSIVE_READ` depending on scope
- large-area sync/discovery must be queued and rate-limited

## Failure behavior

- empty results must be recorded as tool outcomes (not silently ignored)
- conflicting facts across datasets must create competing evidence items and escalation notes
