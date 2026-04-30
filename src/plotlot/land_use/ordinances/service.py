"""Ordinance service wrapper that returns citation-rich results."""

from __future__ import annotations

from plotlot.ingestion.discovery import get_municode_configs
from plotlot.ingestion.scraper import MunicodeScraper
from plotlot.land_use.citations import ordinance_citation
from plotlot.land_use.models import OrdinanceSearchArgs, OrdinanceSearchResult


async def search_municode_live(args: OrdinanceSearchArgs) -> list[OrdinanceSearchResult]:
    """Search Municode for ordinance sections and return cited results."""

    configs = await get_municode_configs()
    muni_key = args.jurisdiction.municipality or args.jurisdiction.county or ""
    config = configs.get(muni_key.lower().replace(" ", "_"))
    if config is None:
        return []

    scraper = MunicodeScraper()
    client = scraper._get_client()  # internal async httpx client
    nodes = await scraper.walk_toc(client, config, config.zoning_node_id, max_depth=3)

    query = args.query.lower()
    results: list[OrdinanceSearchResult] = []
    for node in nodes:
        heading = node.heading or ""
        parent = node.parent_heading or ""
        if query and query not in heading.lower() and query not in parent.lower():
            continue
        html = await scraper.get_section_content(client, config, node.node_id)
        snippet = (html or "").replace("\n", " ")
        snippet = snippet[:300].strip() or heading
        url = f"https://api.municode.com/codescontent?nodeId={node.node_id}"
        citation = ordinance_citation(
            title=heading or "Ordinance section",
            url=url,
            jurisdiction=args.jurisdiction.label(),
            path=[p for p in [parent, heading] if p],
            raw_text_for_hash=f"{config.municipality}:{node.node_id}:{heading}:{snippet}",
        )
        results.append(
            OrdinanceSearchResult(
                section_id=node.node_id,
                heading=heading or "Ordinance section",
                path=[p for p in [parent] if p],
                snippet=snippet or heading or "",
                citation=citation,
            )
        )

        if len(results) >= args.limit:
            break
    return results
