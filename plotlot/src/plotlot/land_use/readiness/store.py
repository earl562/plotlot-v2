"""Transactional versions in existing sites/analysis_runs tables; no DDL.

The light Core table expressions deliberately use the existing column names and
JSON types without importing the application's unrelated ORM model dependencies.
PostgreSQL SELECT FOR UPDATE serializes saves for a site; expected_revision
prevents a user from replacing a version they have not read.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Protocol
from uuid import uuid4

from pydantic import ValidationError
from sqlalchemy import JSON, DateTime, String, column, insert, select, table, update
from sqlalchemy.engine import Result
from sqlalchemy.sql import Executable

from .engine import diff_reports, evaluate
from .models import ReadinessCase, SavedCase

SITES = table(
    "sites", column("id", String), column("workspace_id", String),
    column("project_id", String), column("parcel_id", String), column("facts_json", JSON),
)
RUNS = table(
    "analysis_runs", column("id", String), column("workspace_id", String),
    column("project_id", String), column("site_id", String), column("skill_name", String),
    column("status", String), column("input_json", JSON), column("output_json", JSON),
    column("started_at", DateTime(timezone=True)), column("completed_at", DateTime(timezone=True)),
)


class SessionLike(Protocol):
    async def execute(self, statement: Executable) -> Result[Any]: ...
    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...


class SiteNotFound(ValueError):
    """No site is visible in the requested tenant."""


class RevisionConflict(ValueError):
    """The caller's base version is no longer current."""


class IdentityMismatch(ValueError):
    """The case does not refer to the stored site and parcel."""


class StoredStateInvalid(ValueError):
    """An existing record needs recovery; do not silently replace it."""


def _saved(facts: object) -> SavedCase | None:
    if not isinstance(facts, dict):
        raise StoredStateInvalid("Stored site facts are invalid")
    value = facts.get("site_readiness")
    if value is None:
        return None
    try:
        return SavedCase.model_validate(value)
    except ValidationError as exc:
        raise StoredStateInvalid("Saved readiness state needs recovery") from exc


class ReadinessStore:
    def __init__(self, session: SessionLike):
        self.session = session

    async def _site(self, workspace_id: str, site_id: str, *, lock: bool = False):
        statement = select(SITES).where(
            SITES.c.id == site_id, SITES.c.workspace_id == workspace_id,
        )
        if lock:
            statement = statement.with_for_update()
        row = (await self.session.execute(statement)).mappings().first()
        if row is None:
            raise SiteNotFound("Site not found")
        return row

    async def load(self, workspace_id: str, site_id: str) -> SavedCase | None:
        row = await self._site(workspace_id, site_id)
        return _saved({} if row["facts_json"] is None else row["facts_json"])

    async def save(
        self, workspace_id: str, site_id: str, case: ReadinessCase,
        expected_revision: int, actor_user_id: str,
    ) -> SavedCase:
        try:
            row = await self._site(workspace_id, site_id, lock=True)
            if case.site_id != site_id or case.parcel_id != row["parcel_id"]:
                raise IdentityMismatch("Resolve the stored site and parcel identity before saving")
            facts = {} if row["facts_json"] is None else row["facts_json"]
            previous = _saved(facts)
            revision = previous.revision if previous else 0
            if expected_revision != revision:
                raise RevisionConflict("Readiness changed; reload before saving")
            now = datetime.now(UTC)
            report = evaluate(case, today=now.date())
            saved = SavedCase(
                revision=revision + 1, case=case, report=report,
                changes=diff_reports(previous.report, report) if previous else [],
                updated_at=now.isoformat(), updated_by=actor_user_id, run_id=str(uuid4()),
            )
            value = saved.model_dump(mode="json")
            await self.session.execute(update(SITES).where(
                SITES.c.id == site_id, SITES.c.workspace_id == workspace_id,
            ).values(facts_json={**facts, "site_readiness": value}))
            await self.session.execute(insert(RUNS).values(
                id=saved.run_id, workspace_id=workspace_id, project_id=row["project_id"],
                site_id=site_id, skill_name="site_readiness", status="completed",
                input_json={"case": case.model_dump(mode="json"),
                            "expected_revision": expected_revision},
                output_json=value, started_at=now, completed_at=now,
            ))
            await self.session.commit()
            return saved
        except BaseException:
            await self.session.rollback()
            raise
