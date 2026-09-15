"""Real SQLite persistence tests; PostgreSQL row-lock semantics are a separate gate."""
import asyncio
from importlib import import_module
from pathlib import Path

import pytest
from sqlalchemy import Column, DateTime, JSON, MetaData, String, Table, create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from test_readiness_engine import case_dict, record


def store_module():
    path = Path(__file__).resolve().parents[2] / "src/plotlot/land_use/readiness/store.py"
    assert path.exists(), "Readiness persistence has not been implemented"
    return import_module("plotlot.land_use.readiness.store")


class AsyncSessionAdapter:
    """Exercise production SQL using a real local DB without an async SQLite driver."""
    def __init__(self, session):
        self.session = session

    async def execute(self, statement):
        return self.session.execute(statement)

    async def commit(self):
        self.session.commit()

    async def rollback(self):
        self.session.rollback()


@pytest.fixture
def database():
    metadata = MetaData()
    sites = Table("sites", metadata, Column("id", String, primary_key=True),
                  Column("workspace_id", String), Column("project_id", String),
                  Column("parcel_id", String), Column("facts_json", JSON))
    runs = Table("analysis_runs", metadata, Column("id", String, primary_key=True),
                 Column("workspace_id", String), Column("project_id", String),
                 Column("site_id", String), Column("skill_name", String),
                 Column("status", String), Column("input_json", JSON),
                 Column("output_json", JSON), Column("started_at", DateTime),
                 Column("completed_at", DateTime))
    engine = create_engine("sqlite://", poolclass=StaticPool,
                           connect_args={"check_same_thread": False})
    metadata.create_all(engine)
    session = Session(engine)
    session.execute(sites.insert().values(id="s1", workspace_id="w1", project_id="project1",
                                         parcel_id="p1", facts_json={"existing": "keep"}))
    session.commit()
    yield AsyncSessionAdapter(session), session, sites, runs
    session.close()
    engine.dispose()


def parsed_case(**changes):
    from plotlot.land_use.readiness.models import ReadinessCase
    data = case_dict()
    data.update(changes)
    return ReadinessCase.model_validate(data)


def test_save_load_and_unrelated_facts_survive(database):
    m = store_module()
    adapter, session, sites, runs = database
    store = m.ReadinessStore(adapter)
    saved = asyncio.run(store.save("w1", "s1", parsed_case(), 0, "actor1"))
    loaded = asyncio.run(store.load("w1", "s1"))
    assert saved == loaded
    assert saved.revision == 1
    assert saved.report.decision == "hold"
    assert session.execute(select(sites.c.facts_json)).scalar_one()["existing"] == "keep"
    audit = session.execute(select(runs)).mappings().one()
    assert audit["workspace_id"] == "w1"
    assert audit["input_json"]["case"]["parcel_id"] == "p1"
    assert audit["output_json"]["revision"] == 1


def test_revision_conflict_does_not_overwrite_or_append_run(database):
    m = store_module()
    adapter, session, _, runs = database
    store = m.ReadinessStore(adapter)
    asyncio.run(store.save("w1", "s1", parsed_case(), 0, "actor1"))
    with pytest.raises(m.RevisionConflict):
        asyncio.run(store.save("w1", "s1", parsed_case(), 0, "actor2"))
    assert len(session.execute(select(runs)).all()) == 1
    assert asyncio.run(store.load("w1", "s1")).updated_by == "actor1"


@pytest.mark.parametrize("workspace,site", [("other", "s1"), ("w1", "missing")])
def test_cross_tenant_and_missing_site_are_indistinguishable(database, workspace, site):
    m = store_module()
    store = m.ReadinessStore(database[0])
    with pytest.raises(m.SiteNotFound):
        asyncio.run(store.load(workspace, site))
    with pytest.raises(m.SiteNotFound):
        asyncio.run(store.save(workspace, site, parsed_case(), 0, "actor1"))


def test_stored_parcel_identity_cannot_be_replaced(database):
    m = store_module()
    with pytest.raises(m.IdentityMismatch):
        asyncio.run(m.ReadinessStore(database[0]).save(
            "w1", "s1", parsed_case(parcel_id="wrong"), 0, "actor1"))


def test_case_site_must_match_url_site(database):
    m = store_module()
    with pytest.raises(m.IdentityMismatch):
        asyncio.run(m.ReadinessStore(database[0]).save(
            "w1", "s1", parsed_case(site_id="wrong"), 0, "actor1"))


def test_new_version_retains_prior_audit_and_reports_changes(database):
    m = store_module()
    from datetime import date
    store = m.ReadinessStore(database[0])
    first = asyncio.run(store.save("w1", "s1", parsed_case(), 0, "actor1"))
    second = asyncio.run(store.save("w1", "s1", parsed_case(evidence=[
        record(observed_on=date.today().isoformat())]), 1, "actor2"))
    assert second.revision == 2
    assert second.report.decision == "ready_for_review"
    assert any(c.field == "decision" for c in second.changes)
    rows = database[1].execute(select(database[3])).mappings().all()
    assert len(rows) == 2
    assert next(r for r in rows if r["id"] == first.run_id)["output_json"]["report"]["decision"] == "hold"


def test_failed_audit_write_rolls_back_latest_state(database):
    m = store_module()
    adapter, session, sites, runs = database
    runs.drop(session.get_bind())
    from sqlalchemy.exc import SQLAlchemyError
    with pytest.raises(SQLAlchemyError):
        asyncio.run(m.ReadinessStore(adapter).save("w1", "s1", parsed_case(), 0, "actor1"))
    assert session.execute(select(sites.c.facts_json)).scalar_one() == {"existing": "keep"}


def test_new_site_has_no_saved_readiness_case(database):
    m = store_module()
    assert asyncio.run(m.ReadinessStore(database[0]).load("w1", "s1")) is None


def test_corrupt_saved_state_is_not_silently_overwritten(database):
    m = store_module()
    adapter, session, sites, _ = database
    session.execute(sites.update().values(facts_json={"site_readiness": {"revision": "broken"}}))
    session.commit()
    with pytest.raises(m.StoredStateInvalid):
        asyncio.run(m.ReadinessStore(adapter).save("w1", "s1", parsed_case(), 0, "actor1"))


def test_empty_nonobject_facts_are_not_silently_replaced(database):
    m = store_module()
    adapter, session, sites, _ = database
    session.execute(sites.update().values(facts_json=[]))
    session.commit()
    with pytest.raises(m.StoredStateInvalid):
        asyncio.run(m.ReadinessStore(adapter).save("w1", "s1", parsed_case(), 0, "actor1"))
