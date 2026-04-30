"""Tests for land-use evidence and citation primitives."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from plotlot.land_use import (
    DEFAULT_ORDINANCE_LEGAL_CAVEAT,
    EvidenceBackedReportSection,
    EvidenceCitation,
    EvidenceConfidence,
    EvidenceItem,
    LayerCandidate,
    OrdinanceJurisdiction,
    OrdinanceSearchArgs,
    OrdinanceSearchResult,
    PropertyLayerQuery,
    ReportClaim,
    SourceType,
)


def _retrieved_at() -> datetime:
    return datetime(2026, 4, 30, 15, 0, tzinfo=timezone.utc)


def test_ordinance_citation_adds_legal_caveat():
    citation = EvidenceCitation(
        source_type=SourceType.ORDINANCE,
        title="Off-street parking requirements",
        jurisdiction="Miami-Dade County, FL",
        path=["Code of Ordinances", "Chapter 33", "Parking"],
        url="https://library.municode.com/fl/miami_-_dade_county/codes/code_of_ordinances",
        retrieved_at=_retrieved_at(),
        publisher="Municode/CivicPlus",
    )

    assert citation.legal_caveat == DEFAULT_ORDINANCE_LEGAL_CAVEAT
    assert "Miami-Dade County" in citation.display_label()
    assert "Chapter 33" in citation.display_label()


def test_evidence_item_requires_matching_citation_source_type():
    citation = EvidenceCitation(
        source_type=SourceType.WEB_PAGE,
        title="County page",
        url="https://example.com/source",
        retrieved_at=_retrieved_at(),
    )

    with pytest.raises(ValidationError, match="citation.source_type must match"):
        EvidenceItem(
            id="ev_1",
            workspace_id="ws_1",
            project_id="prj_1",
            claim_key="zoning.district",
            payload={"district": "R-1"},
            source_type=SourceType.ORDINANCE,
            tool_name="search_ordinances",
            confidence=EvidenceConfidence.HIGH,
            citation=citation,
            retrieved_at=_retrieved_at(),
        )


def test_evidence_item_payload_aliases_value_for_prd_examples():
    citation = EvidenceCitation(
        source_type=SourceType.COUNTY_RECORD,
        title="Property Appraiser record",
        url="https://example.com/property",
        retrieved_at=_retrieved_at(),
    )
    evidence = EvidenceItem(
        id="ev_2",
        workspace_id="ws_1",
        project_id="prj_1",
        claim_key="site.owner",
        payload={"owner": "Example Owner LLC"},
        source_type=SourceType.COUNTY_RECORD,
        tool_name="lookup_property_info",
        confidence=EvidenceConfidence.MEDIUM,
        citation=citation,
        retrieved_at=_retrieved_at(),
    )

    assert evidence.value == {"owner": "Example Owner LLC"}


def test_material_report_claims_require_known_evidence_ids():
    with pytest.raises(ValidationError, match="material report claims require"):
        ReportClaim(key="zoning.summary", text="The site permits one unit.")

    with pytest.raises(ValidationError, match="unknown evidence IDs"):
        EvidenceBackedReportSection(
            id="sec_zoning",
            title="Zoning summary",
            evidence_ids=["ev_known"],
            claims=[
                ReportClaim(
                    key="zoning.summary",
                    text="The site permits one unit.",
                    evidence_ids=["ev_missing"],
                )
            ],
        )

    section = EvidenceBackedReportSection(
        id="sec_zoning",
        title="Zoning summary",
        evidence_ids=["ev_known"],
        claims=[
            ReportClaim(
                key="zoning.summary",
                text="The site permits one unit.",
                evidence_ids=["ev_known"],
            )
        ],
    )
    assert section.claims[0].evidence_ids == ["ev_known"]


def test_ordinance_and_open_data_contracts_require_cited_sources():
    ordinance_citation = EvidenceCitation(
        source_type=SourceType.ORDINANCE,
        title="Parking section",
        url="https://library.municode.com/fl/example",
        retrieved_at=_retrieved_at(),
    )
    result = OrdinanceSearchResult(
        section_id="node_123",
        heading="Parking",
        path=["Chapter 33"],
        snippet="Two spaces per dwelling unit.",
        citation=ordinance_citation,
        evidence_id="ev_ord",
    )
    assert result.citation.legal_caveat

    arcgis_citation = EvidenceCitation(
        source_type=SourceType.ARCGIS_LAYER,
        title="Broward Parcels",
        url="https://example.com/FeatureServer/0",
        retrieved_at=_retrieved_at(),
    )
    layer = LayerCandidate(
        id="layer_broward_parcels",
        title="Broward Parcels",
        source_url="https://example.com/item",
        service_url="https://example.com/FeatureServer/0",
        layer_id=0,
        layer_type="parcel",
        field_mapping_confidence=EvidenceConfidence.HIGH,
        citation=arcgis_citation,
    )
    assert layer.layer_type == "parcel"


def test_jurisdiction_and_property_query_require_selectors():
    with pytest.raises(ValidationError, match="county or municipality"):
        OrdinanceJurisdiction(state="fl")

    args = OrdinanceSearchArgs(
        jurisdiction=OrdinanceJurisdiction(state="fl", county="Miami-Dade"),
        query="parking requirements",
    )
    assert args.jurisdiction.state == "FL"

    with pytest.raises(ValidationError, match="address, apn, owner, or bbox"):
        PropertyLayerQuery(county="Broward", state="fl")

    query = PropertyLayerQuery(county="Broward", state="fl", owner="Example LLC")
    assert query.state == "FL"
