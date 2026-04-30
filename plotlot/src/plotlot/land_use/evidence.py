"""Evidence persistence helpers.

This bridges transport-agnostic land-use evidence models to the durable DB
tables created by Alembic 007.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from plotlot.land_use.models import EvidenceItem as LandUseEvidenceItem
from plotlot.storage.models import EvidenceItem


def _now_iso(dt: datetime) -> str:
    return dt.isoformat()


async def persist_land_use_evidence(
    session: AsyncSession,
    *,
    evidence: LandUseEvidenceItem,
) -> EvidenceItem:
    """Persist one land-use evidence item into the durable evidence_items table."""

    row = EvidenceItem(
        id=evidence.id or f"ev_{uuid4()}",
        workspace_id=evidence.workspace_id,
        project_id=evidence.project_id,
        site_id=evidence.site_id,
        analysis_id=evidence.analysis_id,
        analysis_run_id=evidence.analysis_run_id,
        tool_run_id=evidence.tool_run_id,
        claim_key=evidence.claim_key,
        value_json=evidence.payload,
        source_type=evidence.source_type,
        source_url=str(evidence.citation.url) if evidence.citation.url else None,
        source_title=evidence.citation.title,
        source_excerpt=None,
        retrieval_method="hosted_page" if evidence.citation.url else "connector_result",
        trust_label=("high" if evidence.citation.url else "medium"),
        source_version=None,
        content_hash=evidence.citation.raw_source_hash,
        tool_name=evidence.tool_name,
        confidence=evidence.confidence,
        metadata_json={
            "jurisdiction": evidence.citation.jurisdiction,
            "path": evidence.citation.path,
            "publisher": evidence.citation.publisher,
            "legal_caveat": evidence.citation.legal_caveat,
            "retrieved_at": _now_iso(evidence.citation.retrieved_at),
        },
        retrieved_at=evidence.retrieved_at,
    )
    session.add(row)
    await session.flush()
    return row
