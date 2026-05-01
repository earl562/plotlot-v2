"""SQLAlchemy ORM models for pgvector storage."""

from uuid import uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSON, TSVECTOR
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def _uuid() -> str:
    """Return a string UUID for durable workspace-native records."""

    return str(uuid4())


class OrdinanceChunk(Base):
    """A chunk of zoning ordinance text with its embedding vector."""

    __tablename__ = "ordinance_chunks"
    __table_args__ = (
        UniqueConstraint(
            "municipality",
            "municode_node_id",
            "chunk_index",
            name="uq_chunk_natural_key",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    municipality = Column(String(200), nullable=False, index=True)
    county = Column(String(100), nullable=False, index=True)
    chapter = Column(String(500))
    section = Column(String(200))
    section_title = Column(String(500))
    zone_codes: Column = Column(ARRAY(String), default=[])
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, default=0)
    embedding = Column(Vector(1024))
    municode_node_id = Column(String(200))
    search_vector = Column(TSVECTOR)

    # Lineage fields (B2) — provenance tracking for each chunk
    source_url = Column(String, nullable=True)  # Municode URL where this was scraped
    scraped_at = Column(DateTime(timezone=True), nullable=True)  # When it was scraped
    embedding_model = Column(String, nullable=True)  # e.g. "nvidia/nv-embedqa-e5-v5"

    # State/region field (B6) — supports multi-state expansion (FL, NC, etc.)
    state = Column(String(2), nullable=True, default="FL")  # Two-letter state code

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class IngestionCheckpoint(Base):
    """Tracks per-municipality ingestion progress for resumable batch jobs.

    DDIA pattern: idempotent writes with checkpointing. Each municipality
    is a partition — failures are isolated, progress is persistent, and
    the pipeline resumes from where it left off.
    """

    __tablename__ = "ingestion_checkpoints"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String(50), nullable=False, index=True)
    municipality_key = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    status = Column(
        String(20), nullable=False, default="pending"
    )  # pending|running|complete|failed
    chunks_stored = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("batch_id", "municipality_key", name="uq_checkpoint_batch_muni"),
    )


class PortfolioEntry(Base):
    """A saved zoning analysis in the user's portfolio.

    Persists portfolio data across server restarts. The user_id column is
    nullable until auth (Supabase) is wired in — enables per-user filtering
    once authentication is enabled.
    """

    __tablename__ = "portfolio_entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=True, index=True)  # nullable until auth is wired in
    address = Column(String, nullable=False)
    municipality = Column(String, nullable=False)
    county = Column(String, nullable=False)
    zoning_district = Column(String, nullable=True)
    report_json = Column(JSON, nullable=False)  # full ZoningReportResponse as dict
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class ReportCache(Base):
    """Cached zoning report to avoid redundant LLM calls for repeated addresses.

    Reports are stored as JSON with a TTL (default 24h). The address_normalized
    column provides a unique, deterministic cache key derived from the raw address.
    """

    __tablename__ = "report_cache"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False, index=True)
    address_normalized = Column(String, nullable=False, unique=True)  # lowercase, stripped
    report_json = Column(JSON, nullable=False)  # full ZoningReportResponse as dict
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)  # TTL
    hit_count = Column(Integer, default=0)


class UserSubscription(Base):
    """Tracks each user's plan tier and monthly analysis usage.

    Created on first authenticated request.  ``analyses_used`` resets monthly
    via Stripe ``invoice.paid`` webhook or when ``period_end`` has passed.
    """

    __tablename__ = "user_subscriptions"

    user_id = Column(String, primary_key=True)  # Clerk user ID (sub claim)
    plan = Column(String, default="free", nullable=False)  # "free" | "pro"
    stripe_customer_id = Column(String, nullable=True, unique=True)
    stripe_subscription_id = Column(String, nullable=True)
    analyses_used = Column(Integer, default=0, nullable=False)
    period_start = Column(DateTime(timezone=True), nullable=True)
    period_end = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )


class Workspace(Base):
    """Top-level tenant and collaboration boundary."""

    __tablename__ = "workspaces"

    id = Column(String(36), primary_key=True, default=_uuid)
    name = Column(String(200), nullable=False)
    slug = Column(String(120), nullable=True, unique=True)
    owner_user_id = Column(String, nullable=True, index=True)
    settings_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WorkspaceMember(Base):
    """User membership inside a workspace."""

    __tablename__ = "workspace_members"
    __table_args__ = (UniqueConstraint("workspace_id", "user_id", name="uq_workspace_member_user"),)

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    user_id = Column(String, nullable=False, index=True)
    role = Column(String(50), nullable=False, default="member")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    """A land-use or site-feasibility initiative inside a workspace."""

    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(40), nullable=False, default="active", index=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ProjectBranch(Base):
    """Scenario fork for project-level iteration."""

    __tablename__ = "project_branches"
    __table_args__ = (UniqueConstraint("project_id", "name", name="uq_project_branch_name"),)

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String(160), nullable=False)
    parent_branch_id = Column(String(36), ForeignKey("project_branches.id"), nullable=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Site(Base):
    """A parcel, assemblage, or candidate location."""

    __tablename__ = "sites"
    __table_args__ = (UniqueConstraint("project_id", "parcel_id", name="uq_site_project_parcel"),)

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    address = Column(String(300), nullable=False, index=True)
    parcel_id = Column(String(120), nullable=True, index=True)
    geometry_json = Column(JSON, nullable=False, default=dict)
    facts_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Analysis(Base):
    """Durable analysis definition for a project or site."""

    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True, index=True)
    name = Column(String(200), nullable=False)
    skill_name = Column(String(120), nullable=False, index=True)
    status = Column(String(40), nullable=False, default="active", index=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AnalysisRun(Base):
    """One execution of a harness skill or workflow."""

    __tablename__ = "analysis_runs"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True, index=True)
    analysis_id = Column(String(36), ForeignKey("analyses.id"), nullable=True, index=True)
    skill_name = Column(String(120), nullable=False, index=True)
    status = Column(String(40), nullable=False, default="pending", index=True)
    input_json = Column(JSON, nullable=False, default=dict)
    output_json = Column(JSON, nullable=False, default=dict)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EvidenceItem(Base):
    """A source-backed claim recorded by the harness runtime."""

    __tablename__ = "evidence_items"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True, index=True)
    analysis_id = Column(String(36), ForeignKey("analyses.id"), nullable=True, index=True)
    analysis_run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=True, index=True)
    tool_run_id = Column(String(36), ForeignKey("tool_runs.id"), nullable=True, index=True)
    claim_key = Column(String(200), nullable=False, index=True)
    value_json = Column(JSON, nullable=False, default=dict)
    source_type = Column(String(80), nullable=False, index=True)
    source_url = Column(String, nullable=True)
    source_title = Column(String(500), nullable=True)
    source_excerpt = Column(Text, nullable=True)
    retrieval_method = Column(String(80), nullable=False, default="connector_result", index=True)
    trust_label = Column(String(40), nullable=False, default="medium", index=True)
    source_version = Column(String(200), nullable=True)
    content_hash = Column(String(128), nullable=True, index=True)
    tool_name = Column(String(120), nullable=False, index=True)
    confidence = Column(String(40), nullable=False, default="medium", index=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    retrieved_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ToolRun(Base):
    """Audit record for a deterministic tool invocation."""

    __tablename__ = "tool_runs"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True, index=True)
    analysis_id = Column(String(36), ForeignKey("analyses.id"), nullable=True, index=True)
    analysis_run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=True, index=True)
    tool_name = Column(String(120), nullable=False, index=True)
    risk_class = Column(String(40), nullable=False, index=True)
    status = Column(String(40), nullable=False, default="pending", index=True)
    input_json = Column(JSON, nullable=False, default=dict)
    output_json = Column(JSON, nullable=False, default=dict)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ModelRun(Base):
    """Audit record for a model invocation."""

    __tablename__ = "model_runs"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True, index=True)
    analysis_run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=True, index=True)
    provider = Column(String(80), nullable=False, index=True)
    model = Column(String(160), nullable=False, index=True)
    purpose = Column(String(160), nullable=False)
    input_tokens = Column(Integer, nullable=False, default=0)
    output_tokens = Column(Integer, nullable=False, default=0)
    reasoning_tokens = Column(Integer, nullable=False, default=0)
    cost_usd = Column(Float, nullable=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ApprovalRequest(Base):
    """Human approval gate for risky runtime actions."""

    __tablename__ = "approval_requests"

    # Approval IDs are also used as user-facing keys; allow longer deterministic IDs.
    id = Column(String(120), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True, index=True)
    analysis_run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=True, index=True)
    tool_run_id = Column(String(36), ForeignKey("tool_runs.id"), nullable=True, index=True)
    status = Column(String(40), nullable=False, default="pending", index=True)
    risk_class = Column(String(40), nullable=False, index=True)
    action_name = Column(String(160), nullable=False)
    reason = Column(Text, nullable=False)
    request_json = Column(JSON, nullable=False, default=dict)
    response_json = Column(JSON, nullable=False, default=dict)
    requested_by = Column(String, nullable=True, index=True)
    decided_by = Column(String, nullable=True, index=True)
    decided_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Report(Base):
    """Durable report artifact generated from recorded evidence."""

    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True, index=True)
    analysis_run_id = Column(String(36), ForeignKey("analysis_runs.id"), nullable=True, index=True)
    status = Column(String(40), nullable=False, default="draft", index=True)
    report_json = Column(JSON, nullable=False, default=dict)
    evidence_ids: Column = Column(ARRAY(String), nullable=False, default=list)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Document(Base):
    """Exportable document artifact derived from a report."""

    __tablename__ = "documents"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True, index=True)
    report_id = Column(String(36), ForeignKey("reports.id"), nullable=True, index=True)
    document_type = Column(String(80), nullable=False, index=True)
    status = Column(String(40), nullable=False, default="draft", index=True)
    storage_url = Column(String, nullable=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ConnectorAccount(Base):
    """Workspace-scoped account for OAuth/API-key backed connectors."""

    __tablename__ = "connector_accounts"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=False, index=True)
    provider = Column(String(80), nullable=False, index=True)
    auth_type = Column(String(40), nullable=False)
    scopes: Column = Column(ARRAY(String), nullable=False, default=list)
    status = Column(String(40), nullable=False, default="connected", index=True)
    encrypted_credentials_ref = Column(String, nullable=True)
    created_by_user_id = Column(String, nullable=True, index=True)
    metadata_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ConnectorDataset(Base):
    """Discovered public or workspace connector dataset."""

    __tablename__ = "connector_datasets"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=True, index=True)
    provider = Column(String(80), nullable=False, index=True)
    jurisdiction = Column(String(200), nullable=True, index=True)
    topic = Column(String(120), nullable=False, index=True)
    name = Column(String(300), nullable=False)
    endpoint_url = Column(String, nullable=False)
    metadata_url = Column(String, nullable=True)
    license_url = Column(String, nullable=True)
    official_status = Column(String(40), nullable=False, default="unknown", index=True)
    freshness_json = Column(JSON, nullable=False, default=dict)
    schema_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ConnectorSyncRun(Base):
    """Audit record for connector dataset sync/discovery jobs."""

    __tablename__ = "connector_sync_runs"

    id = Column(String(36), primary_key=True, default=_uuid)
    workspace_id = Column(String(36), ForeignKey("workspaces.id"), nullable=True, index=True)
    connector_account_id = Column(
        String(36), ForeignKey("connector_accounts.id"), nullable=True, index=True
    )
    connector_dataset_id = Column(
        String(36), ForeignKey("connector_datasets.id"), nullable=True, index=True
    )
    status = Column(String(40), nullable=False, default="pending", index=True)
    counts_json = Column(JSON, nullable=False, default=dict)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GoldSetCase(Base):
    """Durable eval/golden case for zoning and site-feasibility workflows."""

    __tablename__ = "gold_set_cases"

    id = Column(String(36), primary_key=True, default=_uuid)
    suite = Column(String(120), nullable=False, index=True)
    case_id = Column(String(160), nullable=False, unique=True)
    jurisdiction = Column(String(200), nullable=False, index=True)
    address = Column(String(300), nullable=True)
    expected_json = Column(JSON, nullable=False, default=dict)
    source_urls: Column = Column(ARRAY(String), nullable=False, default=list)
    tags: Column = Column(ARRAY(String), nullable=False, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EvalRun(Base):
    """One eval run against a gold-set suite."""

    __tablename__ = "eval_runs"

    id = Column(String(36), primary_key=True, default=_uuid)
    suite = Column(String(120), nullable=False, index=True)
    git_sha = Column(String(80), nullable=True, index=True)
    model_profile = Column(String(160), nullable=True)
    status = Column(String(40), nullable=False, default="pending", index=True)
    metrics_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)


class EvalCaseResult(Base):
    """Per-case result for trajectory-aware eval scoring."""

    __tablename__ = "eval_case_results"

    id = Column(String(36), primary_key=True, default=_uuid)
    eval_run_id = Column(String(36), ForeignKey("eval_runs.id"), nullable=False, index=True)
    gold_set_case_id = Column(
        String(36), ForeignKey("gold_set_cases.id"), nullable=False, index=True
    )
    status = Column(String(40), nullable=False, index=True)
    diffs_json = Column(JSON, nullable=False, default=dict)
    evidence_metrics_json = Column(JSON, nullable=False, default=dict)
    trajectory_metrics_json = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
