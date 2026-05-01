"""Default harness runtime wiring.

This is the shared execution seam for REST tool routes and the MCP adapter.
Chat currently uses bespoke tool execution; the long-term goal is to route chat
through this runtime too.
"""

from __future__ import annotations

import uuid
from typing import Any

from plotlot.harness.policy import HarnessPolicyEngine
from plotlot.harness.runtime import HarnessRuntime
from plotlot.land_use.models import (
    EvidenceConfidence,
    EvidenceBackedReportSection,
    EvidenceItem,
    OrdinanceJurisdiction,
    OrdinanceSearchArgs,
    ReportClaim,
    SourceType,
    ToolContext,
)
from plotlot.land_use.policy import ToolPolicy


def _ev_id() -> str:
    return str(uuid.uuid4())


async def _handle_geocode_address(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    from plotlot.retrieval.geocode import geocode_address
    from plotlot.land_use.citations import geocode_citation

    address = str(args.get("address", "")).strip()
    try:
        result = await geocode_address(address)
    except Exception as e:
        return {"status": "error", "message": f"Geocoding failed: {type(e).__name__}: {e}"}
    if not result:
        return {"status": "not_found", "result": {}}

    ev_id = _ev_id()
    citation = geocode_citation(
        title="Geocoding result",
        publisher="Geocodio/Census",
        raw_text_for_hash=f"{address}:{result.get('lat')}:{result.get('lng')}",
    )
    evidence_item = EvidenceItem(
        id=ev_id,
        workspace_id=context.workspace_id,
        project_id=context.project_id or "prj_unknown",
        site_id=context.site_id,
        analysis_id=context.analysis_id,
        analysis_run_id=context.analysis_run_id,
        tool_run_id=context.tool_run_id,
        claim_key="site.geocode",
        payload={"address": address, **result},
        source_type=SourceType.WEB_PAGE,
        tool_name="geocode_address",
        confidence=EvidenceConfidence.MEDIUM,
        citation=citation,
    )

    return {
        "status": "success",
        "result": result,
        "evidence": [evidence_item.model_dump(mode="json")],
    }


async def _handle_lookup_property_info(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    from plotlot.retrieval.property import lookup_property
    from plotlot.land_use.citations import county_record_citation

    address = str(args.get("address", "")).strip()
    county = str(args.get("county", "")).strip()

    def _to_float_or_none(value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    lat = _to_float_or_none(args.get("lat"))
    lng = _to_float_or_none(args.get("lng"))

    try:
        record = await lookup_property(address, county, lat=lat, lng=lng)
    except Exception as e:
        return {"status": "error", "message": f"Property lookup failed: {type(e).__name__}: {e}"}
    if not record:
        return {"status": "not_found", "result": {}}

    payload: dict[str, Any] = {
        "folio": record.folio,
        "address": record.address,
        "municipality": record.municipality,
        "county": record.county,
        "owner": record.owner,
        "zoning_code": record.zoning_code,
        "zoning_description": record.zoning_description,
        "lot_size_sqft": record.lot_size_sqft,
        "lot_dimensions": record.lot_dimensions,
        "year_built": record.year_built,
        "assessed_value": record.assessed_value,
        "lat": record.lat,
        "lng": record.lng,
        "zoning_layer_url": record.zoning_layer_url,
    }

    result: dict[str, Any] = {"status": "success", "result": payload}

    ev_id = _ev_id()
    citation = county_record_citation(
        title="County property appraiser record",
        url=record.zoning_layer_url or None,
        jurisdiction=record.county,
        publisher=None,
        raw_text_for_hash=f"{record.folio}:{record.owner}:{record.zoning_code}:{record.lot_size_sqft}",
    )
    evidence_item = EvidenceItem(
        id=ev_id,
        workspace_id=context.workspace_id,
        project_id=context.project_id or "prj_unknown",
        site_id=context.site_id,
        analysis_id=context.analysis_id,
        analysis_run_id=context.analysis_run_id,
        tool_run_id=context.tool_run_id,
        claim_key="site.property_record",
        payload=payload,
        source_type=SourceType.COUNTY_RECORD,
        tool_name="lookup_property_info",
        confidence=EvidenceConfidence.MEDIUM,
        citation=citation,
    )

    result["evidence"] = [evidence_item.model_dump(mode="json")]
    return result


async def _handle_search_zoning_ordinance(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    """Search locally indexed ordinance chunks and return cited results.

    This produces evidence items so downstream reports can reference `evidence_id`s
    rather than uncited prose.
    """

    from plotlot.retrieval.search import hybrid_search
    from plotlot.storage.db import get_session
    from plotlot.land_use.citations import ordinance_citation

    municipality = str(args.get("municipality", "")).strip()
    query = str(args.get("query", "")).strip()

    session = await get_session()
    try:
        results = await hybrid_search(session, municipality, query, limit=8)

        out: list[dict[str, Any]] = []
        evidence: list[dict[str, Any]] = []

        for r in results:
            ev_id = _ev_id()
            source_url = getattr(r, "source_url", None)
            municode_node_id = getattr(r, "municode_node_id", None)
            if not source_url and municode_node_id:
                source_url = f"https://api.municode.com/codescontent?nodeId={municode_node_id}"

            citation = ordinance_citation(
                title=(r.section_title or r.section or "Ordinance section"),
                url=source_url,
                jurisdiction=municipality,
                path=[p for p in [getattr(r, "chapter", None), r.section] if p],
                raw_text_for_hash=f"{municipality}:{r.section}:{r.section_title}:{r.chunk_text[:300]}",
            )
            out.append(
                {
                    "section": r.section,
                    "title": r.section_title,
                    "zone_codes": r.zone_codes,
                    "text": r.chunk_text,
                    "evidence_id": ev_id,
                    "citation": citation.model_dump(mode="json"),
                }
            )
            evidence_item = EvidenceItem(
                id=ev_id,
                workspace_id=context.workspace_id,
                project_id=context.project_id or "prj_unknown",
                site_id=context.site_id,
                analysis_id=context.analysis_id,
                analysis_run_id=context.analysis_run_id,
                tool_run_id=context.tool_run_id,
                claim_key="ordinance.chunk",
                payload={
                    "municipality": municipality,
                    "query": query,
                    "section": r.section,
                    "section_title": r.section_title,
                    "chunk_text": r.chunk_text,
                },
                source_type=SourceType.ORDINANCE,
                tool_name="search_zoning_ordinance",
                confidence=EvidenceConfidence.MEDIUM,
                citation=citation,
            )
            evidence.append(evidence_item.model_dump(mode="json"))

        return {"status": "success", "results": out, "evidence": evidence}
    finally:
        await session.close()


async def _handle_search_municode_live(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    from plotlot.land_use.ordinances.service import search_municode_live

    municipality = str(args.get("municipality", "")).strip()
    query = str(args.get("query", "")).strip()

    results = await search_municode_live(
        OrdinanceSearchArgs(
            jurisdiction=OrdinanceJurisdiction(state="FL", municipality=municipality),
            query=query,
            limit=int(args.get("limit", 8) or 8),
        )
    )

    evidence: list[dict[str, Any]] = []
    out: list[dict[str, Any]] = []
    for r in results:
        ev_id = _ev_id()
        r = r.model_copy(update={"evidence_id": ev_id})
        out.append(r.model_dump(mode="json"))
        evidence_item = EvidenceItem(
            id=ev_id,
            workspace_id=context.workspace_id,
            project_id=context.project_id or "prj_unknown",
            site_id=context.site_id,
            analysis_id=context.analysis_id,
            analysis_run_id=context.analysis_run_id,
            tool_run_id=context.tool_run_id,
            claim_key="ordinance.section",
            payload={
                "section_id": r.section_id,
                "heading": r.heading,
                "path": r.path,
                "snippet": r.snippet,
            },
            source_type=SourceType.ORDINANCE,
            tool_name="search_municode_live",
            confidence=EvidenceConfidence.MEDIUM,
            citation=r.citation,
        )
        evidence.append(evidence_item.model_dump(mode="json"))

    return {"status": "success", "results": out, "evidence": evidence}


async def _handle_discover_open_data_layers(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    from plotlot.land_use.open_data.service import discover_layers
    from plotlot.land_use.models import LayerCandidate

    county = str(args.get("county", "")).strip()
    state = str(args.get("state", "FL")).strip() or "FL"
    lat_raw = args.get("lat")
    lng_raw = args.get("lng")
    if lat_raw is None or lng_raw is None:
        return {
            "status": "error",
            "message": "discover_open_data_layers requires numeric lat and lng",
            "results": [],
            "evidence": [],
        }
    try:
        lat = float(lat_raw)
        lng = float(lng_raw)
    except (TypeError, ValueError):
        return {
            "status": "error",
            "message": "discover_open_data_layers requires numeric lat and lng",
            "results": [],
            "evidence": [],
        }

    candidates = await discover_layers(county=county, state=state, lat=lat, lng=lng)

    evidence: list[dict[str, Any]] = []
    out: list[dict[str, Any]] = []
    for c in candidates:
        ev_id = _ev_id()
        c = LayerCandidate.model_validate(c).model_copy(update={"evidence_id": ev_id})
        out.append(c.model_dump(mode="json"))
        evidence_item = EvidenceItem(
            id=ev_id,
            workspace_id=context.workspace_id,
            project_id=context.project_id or "prj_unknown",
            site_id=context.site_id,
            analysis_id=context.analysis_id,
            analysis_run_id=context.analysis_run_id,
            tool_run_id=context.tool_run_id,
            claim_key="open_data.layer",
            payload={
                "id": c.id,
                "title": c.title,
                "service_url": str(c.service_url),
                "source_url": str(c.source_url),
                "layer_id": c.layer_id,
                "layer_type": c.layer_type,
            },
            source_type=SourceType.ARCGIS_LAYER,
            tool_name="discover_open_data_layers",
            confidence=c.field_mapping_confidence,
            citation=c.citation,
        )
        evidence.append(evidence_item.model_dump(mode="json"))

    return {"status": "success", "results": out, "evidence": evidence}


async def _handle_generate_document(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    """Generate an internal evidence-backed report artifact.

    This does not perform external writes; it returns artifact payloads for the
    REST adapter to persist into durable tables.
    """

    title = str(args.get("title") or "Evidence-backed report").strip()
    evidence_ids = list(args.get("evidence_ids") or [])
    evidence_ids = [str(e).strip() for e in evidence_ids if str(e).strip()]
    if not evidence_ids:
        return {
            "status": "error",
            "message": "generate_document requires evidence_ids",
            "artifacts": {},
        }

    section = EvidenceBackedReportSection(
        id="sec_evidence",
        title="Evidence",
        evidence_ids=evidence_ids,
        claims=[
            ReportClaim(
                key=f"evidence.{i}",
                text=f"Supported by evidence item {evidence_id}.",
                evidence_ids=[evidence_id],
            )
            for i, evidence_id in enumerate(evidence_ids, start=1)
        ],
    )

    report_json = {
        "title": title,
        "generated_by": "generate_document",
        "sections": [section.model_dump()],
        "evidence_ids": evidence_ids,
    }

    return {
        "status": "success",
        "report": report_json,
        "artifacts": {
            "report": {
                "status": "draft",
                "report_json": report_json,
                "evidence_ids": evidence_ids,
            },
            "document": {
                "document_type": "evidence_report",
                "status": "draft",
                "metadata_json": {"title": title},
            },
        },
    }


async def _handle_draft_google_doc(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    """Create an internal document draft (no external connector write)."""

    title = str(args.get("title", "")).strip() or "Untitled Draft"
    content = str(args.get("content", "") or "").strip()
    evidence_ids = args.get("evidence_ids") or []
    if not isinstance(evidence_ids, list):
        evidence_ids = []

    draft_id = f"draft_doc_{uuid.uuid4()}"
    preview = content[:240]

    return {
        "status": "drafted",
        "draft": {
            "draft_id": draft_id,
            "title": title,
            "content_preview": preview,
            "evidence_ids": evidence_ids,
        },
        "artifacts": {
            "document": {
                "document_type": "google_doc_draft",
                "status": "draft",
                "metadata_json": {
                    "draft_id": draft_id,
                    "title": title,
                    "content": content,
                    "evidence_ids": evidence_ids,
                    "workspace_id": context.workspace_id,
                    "project_id": context.project_id,
                    "site_id": context.site_id,
                },
            }
        },
    }


async def _handle_draft_email(args: dict[str, Any], context: ToolContext) -> dict[str, Any]:
    """Create an internal outreach email draft (no external connector write)."""

    to_raw = args.get("to") or []
    to_list = to_raw if isinstance(to_raw, list) else [str(to_raw)]
    to_list = [str(addr).strip() for addr in to_list if str(addr).strip()]
    subject = str(args.get("subject", "") or "").strip()
    body = str(args.get("body", "") or "").strip()
    evidence_ids = args.get("evidence_ids") or []
    if not isinstance(evidence_ids, list):
        evidence_ids = []

    draft_id = f"draft_email_{uuid.uuid4()}"
    preview = body[:240]

    return {
        "status": "drafted",
        "draft": {
            "draft_id": draft_id,
            "to": to_list,
            "subject": subject,
            "body_preview": preview,
            "evidence_ids": evidence_ids,
        },
        "artifacts": {
            "document": {
                "document_type": "email_draft",
                "status": "draft",
                "metadata_json": {
                    "draft_id": draft_id,
                    "to": to_list,
                    "subject": subject,
                    "body": body,
                    "evidence_ids": evidence_ids,
                    "workspace_id": context.workspace_id,
                    "project_id": context.project_id,
                    "site_id": context.site_id,
                },
            }
        },
    }


def build_default_runtime() -> HarnessRuntime:
    policy = HarnessPolicyEngine(
        policy=ToolPolicy(
            internal_write_tools=frozenset({"draft_email", "draft_google_doc", "generate_document"})
        )
    )
    runtime = HarnessRuntime(policy=policy)
    runtime.register("geocode_address", _handle_geocode_address)
    runtime.register("lookup_property_info", _handle_lookup_property_info)
    runtime.register("search_zoning_ordinance", _handle_search_zoning_ordinance)
    runtime.register("search_municode_live", _handle_search_municode_live)
    runtime.register("discover_open_data_layers", _handle_discover_open_data_layers)
    runtime.register("draft_google_doc", _handle_draft_google_doc)
    runtime.register("draft_email", _handle_draft_email)
    runtime.register("generate_document", _handle_generate_document)
    return runtime


_DEFAULT_RUNTIME: HarnessRuntime | None = None


def get_default_runtime() -> HarnessRuntime:
    global _DEFAULT_RUNTIME
    if _DEFAULT_RUNTIME is None:
        _DEFAULT_RUNTIME = build_default_runtime()
    return _DEFAULT_RUNTIME
