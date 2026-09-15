"""Draft site-readiness previews and authenticated, tenant-scoped saved versions."""
from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import SQLAlchemyError

from plotlot.land_use.readiness.engine import evaluate
from plotlot.land_use.readiness.models import ReadinessCase, ReadinessReport, SavedCase, SaveRequest
from plotlot.land_use.readiness.playbooks import Playbook, requirements_for
from plotlot.land_use.readiness.store import (
    IdentityMismatch, ReadinessStore, RevisionConflict, SessionLike, SiteNotFound, StoredStateInvalid,
)

router = APIRouter(tags=["site-readiness"])
DATABASE_UNAVAILABLE_MESSAGE = "Readiness storage is unavailable. No success is being reported."


def require_actor(request: Request, workspace_id: str) -> str:
    actor = getattr(request.state, "actor", None)
    user_id = getattr(actor, "user_id", None)
    if not isinstance(user_id, str) or not user_id.strip():
        raise HTTPException(401, "Authentication required for saved readiness cases")
    if getattr(actor, "tenant_id", None) != workspace_id:
        raise HTTPException(403, "Cross-tenant access denied")
    return user_id


async def readiness_session(request: Request, workspace_id: str):
    # Authenticate before creating a DB session, including in auth-disabled development.
    require_actor(request, workspace_id)
    from plotlot.storage.db import get_session

    session = None
    try:
        session = await get_session()
        yield session
    except (SQLAlchemyError, ConnectionError, TimeoutError) as exc:
        raise HTTPException(503, DATABASE_UNAVAILABLE_MESSAGE) from exc
    finally:
        if session is not None:
            await session.close()


@router.get("/readiness/playbooks/{kind}")
def playbook(kind: Playbook, response: Response):
    response.headers["Cache-Control"] = "no-store"
    return {
        "kind": kind,
        "scope": "starter_checklist_not_jurisdictional_determination",
        "requirements": requirements_for(kind),
    }


@router.post("/readiness/preview", response_model=ReadinessReport)
def preview(case: ReadinessCase, response: Response) -> ReadinessReport:
    response.headers["Cache-Control"] = "no-store"
    return evaluate(case)


@router.get("/readiness/workbench", response_class=HTMLResponse)
def workbench() -> HTMLResponse:
    nonce = secrets.token_urlsafe(24)
    path = Path(__file__).resolve().parents[1] / "land_use/readiness/workbench.html"
    return HTMLResponse(path.read_text().replace("__NONCE__", nonce), headers={
        "Cache-Control": "no-store",
        "Content-Security-Policy": (
            "default-src 'none'; connect-src 'self'; base-uri 'none'; frame-ancestors 'none'; "
            f"script-src 'nonce-{nonce}'; style-src 'nonce-{nonce}'; "
            "form-action 'none'; img-src data:"
        ),
        "X-Content-Type-Options": "nosniff",
    })


@router.get("/workspaces/{workspace_id}/sites/{site_id}/readiness", response_model=SavedCase)
async def load_readiness(
    request: Request, workspace_id: str, site_id: str, response: Response,
    session: Annotated[SessionLike, Depends(readiness_session)],
) -> SavedCase:
    require_actor(request, workspace_id)
    response.headers["Cache-Control"] = "no-store"
    try:
        saved = await ReadinessStore(session).load(workspace_id, site_id)
        if saved is None:
            raise HTTPException(404, "No saved readiness case")
        return saved
    except SiteNotFound as exc:
        raise HTTPException(404, "Site not found") from exc
    except StoredStateInvalid as exc:
        raise HTTPException(409, "Saved readiness state needs recovery") from exc
    except SQLAlchemyError as exc:
        raise HTTPException(503, DATABASE_UNAVAILABLE_MESSAGE) from exc


@router.put("/workspaces/{workspace_id}/sites/{site_id}/readiness", response_model=SavedCase)
async def save_readiness(
    request: Request, workspace_id: str, site_id: str, body: SaveRequest, response: Response,
    session: Annotated[SessionLike, Depends(readiness_session)],
) -> SavedCase:
    actor_user_id = require_actor(request, workspace_id)
    response.headers["Cache-Control"] = "no-store"
    try:
        return await ReadinessStore(session).save(
            workspace_id, site_id, body.case, body.expected_revision, actor_user_id,
        )
    except SiteNotFound as exc:
        raise HTTPException(404, "Site not found") from exc
    except (RevisionConflict, IdentityMismatch, StoredStateInvalid) as exc:
        raise HTTPException(409, str(exc)) from exc
    except SQLAlchemyError as exc:
        raise HTTPException(503, DATABASE_UNAVAILABLE_MESSAGE) from exc
