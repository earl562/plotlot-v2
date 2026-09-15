"""Isolated actual ASGI route tests; production middleware regression is separate."""
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from test_readiness_engine import case_dict
from test_readiness_store import database  # noqa: F401 -- shared DB fixture


def api_module():
    path = Path(__file__).resolve().parents[2] / "src/plotlot/api/readiness.py"
    assert path.exists(), "Readiness API has not been implemented"
    return import_module("plotlot.api.readiness")


def client_for(database=None, actor=None):
    api = api_module()
    app = FastAPI()
    if actor is not None:
        @app.middleware("http")
        async def verified_test_identity(request: Request, call_next):
            request.state.actor = actor
            return await call_next(request)
    if database is not None:
        async def session_override():
            yield database[0]
        app.dependency_overrides[api.readiness_session] = session_override
    app.include_router(api.router, prefix="/api/v1")
    return TestClient(app)


def test_preview_runs_without_database_or_network():
    with client_for() as client:
        response = client.post("/api/v1/readiness/preview", json=case_dict())
    assert response.status_code == 200
    assert response.json()["decision"] == "hold"
    assert response.headers["cache-control"] == "no-store"


def test_preview_validates_payload_instead_of_ignoring_extra_fields():
    data = case_dict()
    data["approved"] = True
    with client_for() as client:
        assert client.post("/api/v1/readiness/preview", json=data).status_code == 422


@pytest.mark.parametrize("kind,count", [("residential", 8), ("industrial", 8), ("data_center", 11)])
def test_playbooks_are_explicit_starters(kind, count):
    with client_for() as client:
        response = client.get(f"/api/v1/readiness/playbooks/{kind}")
    assert response.status_code == 200
    assert len(response.json()["requirements"]) == count
    assert response.json()["scope"] == "starter_checklist_not_jurisdictional_determination"


def test_unknown_playbook_rejected():
    with client_for() as client:
        assert client.get("/api/v1/readiness/playbooks/unknown").status_code == 422


@pytest.mark.parametrize("method", ["get", "put"])
def test_persistence_requires_identity_even_without_global_middleware(database, method):
    with client_for(database) as client:
        args = {"json": {"case": case_dict(), "expected_revision": 0}} if method == "put" else {}
        response = getattr(client, method)("/api/v1/workspaces/w1/sites/s1/readiness", **args)
    assert response.status_code == 401


def test_cross_tenant_actor_cannot_read_or_write(database):
    actor = SimpleNamespace(tenant_id="other", user_id="actor1")
    with client_for(database, actor) as client:
        url = "/api/v1/workspaces/w1/sites/s1/readiness"
        assert client.get(url).status_code == 403
        assert client.put(url, json={"case": case_dict(), "expected_revision": 0}).status_code == 403


def test_save_and_reload_through_actual_api(database):
    actor = SimpleNamespace(tenant_id="w1", user_id="actor1")
    with client_for(database, actor) as client:
        url = "/api/v1/workspaces/w1/sites/s1/readiness"
        assert client.get(url).status_code == 404
        saved = client.put(url, json={"case": case_dict(), "expected_revision": 0})
        assert saved.status_code == 200
        assert saved.json()["revision"] == 1
        assert client.get(url).json() == saved.json()
        assert client.put(url, json={"case": case_dict(), "expected_revision": 0}).status_code == 409


def test_negative_or_boolean_revision_rejected(database):
    actor = SimpleNamespace(tenant_id="w1", user_id="actor1")
    with client_for(database, actor) as client:
        for revision in [-1, True]:
            assert client.put("/api/v1/workspaces/w1/sites/s1/readiness",
                              json={"case": case_dict(), "expected_revision": revision}).status_code == 422


def test_database_failure_is_sanitized():
    from sqlalchemy.exc import SQLAlchemyError
    api = api_module()
    app = FastAPI()
    @app.middleware("http")
    async def actor(request, call_next):
        request.state.actor = SimpleNamespace(tenant_id="w1", user_id="actor1")
        return await call_next(request)
    class FailedSession:
        async def execute(self, statement):
            raise SQLAlchemyError("secret database URL and credentials")
        async def rollback(self):
            pass
    async def failing_session():
        yield FailedSession()
    app.dependency_overrides[api.readiness_session] = failing_session
    app.include_router(api.router, prefix="/api/v1")
    with TestClient(app) as client:
        result = client.get("/api/v1/workspaces/w1/sites/s1/readiness")
    assert result.status_code == 503
    assert "secret" not in result.text
    assert result.json()["detail"] == api.DATABASE_UNAVAILABLE_MESSAGE


def test_workbench_is_draft_labeled_and_has_nonce_csp():
    with client_for() as client:
        result = client.get("/api/v1/readiness/workbench")
    assert result.status_code == 200
    assert "Structured evidence" in result.text
    assert "DRAFT" in result.text
    assert "nonce-" in result.headers["content-security-policy"]
    assert "frame-ancestors 'none'" in result.headers["content-security-policy"]
    assert "__NONCE__" not in result.text
    assert result.headers["cache-control"] == "no-store"


def test_workspace_router_mounts_readiness_without_new_main_app_rewrite():
    import ast
    path = Path(__file__).resolve().parents[2] / "src/plotlot/api/workspaces.py"
    tree = ast.parse(path.read_text())
    imports = [n for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)]
    assert any(n.module == "plotlot.api.readiness" for n in imports)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    assert any(isinstance(n.func, ast.Attribute) and n.func.attr == "include_router"
               and any(isinstance(a, ast.Name) and a.id == "readiness_router" for a in n.args)
               for n in calls)
