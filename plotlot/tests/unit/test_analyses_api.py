"""Unit tests for the Analysis + AnalysisRun lifecycle API."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest


class FakeSession:
    def __init__(self):  # noqa: D401
        self._workspaces: dict[str, object] = {}
        self._projects: dict[str, object] = {}
        self._analyses: dict[str, object] = {}
        self._runs: dict[str, object] = {}

    async def get(self, model, key):  # noqa: ANN001
        name = getattr(model, "__name__", "")
        if name == "Workspace":
            return self._workspaces.get(key)
        if name == "Project":
            return self._projects.get(key)
        if name == "Analysis":
            return self._analyses.get(key)
        if name == "AnalysisRun":
            return self._runs.get(key)
        return None

    def add(self, obj):  # noqa: ANN001
        name = obj.__class__.__name__
        if name == "Analysis":
            self._analyses[getattr(obj, "id")] = obj
        if name == "AnalysisRun":
            self._runs[getattr(obj, "id")] = obj

    async def flush(self):
        return None

    async def commit(self):
        return None

    async def close(self):
        return None


@pytest.mark.asyncio
async def test_analysis_lifecycle_create_and_run(client):
    from plotlot.storage.models import Project, Workspace

    session = FakeSession()
    session._workspaces["ws_test"] = Workspace(id="ws_test", name="Test WS")  # type: ignore[arg-type]
    session._projects["prj_test"] = Project(
        id="prj_test",
        workspace_id="ws_test",
        name="Project",
    )  # type: ignore[arg-type]

    with patch("plotlot.api.analyses.get_session", new=AsyncMock(return_value=session)):
        resp = await client.post(
            "/api/v1/analyses",
            json={
                "workspace_id": "ws_test",
                "project_id": "prj_test",
                "name": "Zoning sweep",
                "skill_name": "zoning_research",
                "metadata_json": {"kind": "unit"},
            },
        )
        assert resp.status_code == 200
        created = resp.json()
        analysis_id = created["id"]
        assert created["workspace_id"] == "ws_test"
        assert created["project_id"] == "prj_test"
        assert created["skill_name"] == "zoning_research"

        resp = await client.get(f"/api/v1/analyses/{analysis_id}")
        assert resp.status_code == 200
        fetched = resp.json()
        assert fetched["id"] == analysis_id
        assert fetched["status"] == "active"

        resp = await client.post(
            f"/api/v1/analyses/{analysis_id}/runs",
            json={"input_json": {"prompt": "hello"}},
        )
        assert resp.status_code == 200
        run = resp.json()
        run_id = run["id"]
        assert run["analysis_id"] == analysis_id
        assert run["status"] == "pending"
        assert run["input_json"]["prompt"] == "hello"

        resp = await client.get(f"/api/v1/analysis-runs/{run_id}")
        assert resp.status_code == 200
        fetched_run = resp.json()
        assert fetched_run["id"] == run_id
        assert fetched_run["analysis_id"] == analysis_id
