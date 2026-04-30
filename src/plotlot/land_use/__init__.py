"""Land-use harness primitives.

This package contains the first executable seam for the agentic land-use
consultant harness: typed evidence, citations, tool contracts, policy decisions,
and gold-set fixtures. The modules are intentionally transport-agnostic so the
same contracts can back REST, chat tools, and future MCP adapters.
"""

from plotlot.land_use.goldset import GoldCase, GoldSet, load_land_use_goldset
from plotlot.land_use.models import (
    DEFAULT_ORDINANCE_LEGAL_CAVEAT,
    EvidenceBackedReportSection,
    EvidenceCitation,
    EvidenceConfidence,
    EvidenceItem,
    LayerCandidate,
    OrdinanceJurisdiction,
    OrdinanceSearchArgs,
    OrdinanceSearchResult,
    PolicyDecision,
    PropertyLayerQuery,
    ReportClaim,
    SourceType,
    ToolContext,
    ToolContract,
    ToolRiskClass,
)
from plotlot.land_use.policy import ToolPolicy

__all__ = [
    "DEFAULT_ORDINANCE_LEGAL_CAVEAT",
    "EvidenceBackedReportSection",
    "EvidenceCitation",
    "EvidenceConfidence",
    "EvidenceItem",
    "GoldCase",
    "GoldSet",
    "LayerCandidate",
    "OrdinanceJurisdiction",
    "OrdinanceSearchArgs",
    "OrdinanceSearchResult",
    "PolicyDecision",
    "PropertyLayerQuery",
    "ReportClaim",
    "SourceType",
    "ToolContext",
    "ToolContract",
    "ToolPolicy",
    "ToolRiskClass",
    "load_land_use_goldset",
]
