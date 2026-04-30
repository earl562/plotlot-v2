# Municode Connector Contract

## Purpose

Expose ordinance discovery/search/section retrieval to PlotLot tools while recording citation-grade provenance. Municode is treated as a useful surface, not the legal system of record.

## Retrieval posture

PlotLot must label upstream retrieval method and trust for every ordinance evidence item:

| Method | Trust posture | Product behavior |
|---|---|---|
| `official_export` | Highest | Prefer when available; cache by version/hash |
| `hosted_page` | High | Citable ordinance page; store excerpt + retrieval timestamp |
| `unofficial_endpoint` | Medium | Use only behind connector; resolve hosted-page citations when possible |
| `browser_capture` | Low | Fallback only; require report warning + human review for trust-critical claims |

## Tool contracts (conceptual)

- `search_ordinances(jurisdiction, query, limit) -> [OrdinanceSearchResult]`
- `fetch_ordinance_section(jurisdiction, section_id) -> OrdinanceSection`

## Evidence requirements

Every ordinance evidence item used in a report must include:

- source URL
- retrieved timestamp
- publisher (when known)
- jurisdiction label
- path (toc path) when known
- legal caveat (required for ordinances)
- raw source hash / content hash

## Governance

- ordinance search/read is `READ_ONLY`
- bulk crawling is `EXPENSIVE_READ` (rate-limited, queued)
- any report relying on low-trust ordinance evidence must require human review

## Failure behavior

- if no citable source URL is available, return an unresolved result instead of fabricating a citation
- if codification freshness is unknown, mark evidence as stale-risk and require report warning
