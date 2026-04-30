"""Workspace/project/site API.

This is the minimal CRUD surface needed to make the harness distribution model
real: users operate inside a workspace, which contains projects and sites.
"""

from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select

from plotlot.storage.db import get_session
from plotlot.storage.models import Project, Site, Workspace


router = APIRouter(prefix="/api/v1", tags=["workspace"])


class WorkspaceCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    slug: str | None = Field(default=None, max_length=120)


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None


class SiteCreateRequest(BaseModel):
    address: str = Field(..., min_length=5, max_length=300)
    parcel_id: str | None = Field(default=None, max_length=120)


@router.get("/workspaces")
async def list_workspaces():
    session = await get_session()
    try:
        result = await session.execute(select(Workspace).order_by(Workspace.created_at.asc()))
        rows = result.scalars().all()
        return [
            {
                "id": w.id,
                "name": w.name,
                "slug": w.slug,
            }
            for w in rows
        ]
    finally:
        await session.close()


@router.post("/workspaces")
async def create_workspace(body: WorkspaceCreateRequest):
    session = await get_session()
    try:
        ws = Workspace(id=str(uuid4()), name=body.name, slug=body.slug)
        session.add(ws)
        await session.flush()
        await session.commit()
        return {"id": ws.id, "name": ws.name, "slug": ws.slug}
    finally:
        await session.close()


@router.get("/workspaces/{workspace_id}/projects")
async def list_projects(workspace_id: str):
    session = await get_session()
    try:
        ws = await session.get(Workspace, workspace_id)
        if ws is None:
            raise HTTPException(status_code=404, detail="Workspace not found")
        result = await session.execute(
            select(Project)
            .where(Project.workspace_id == workspace_id)
            .order_by(Project.created_at.asc())
        )
        rows = result.scalars().all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "status": p.status,
            }
            for p in rows
        ]
    finally:
        await session.close()


@router.post("/workspaces/{workspace_id}/projects")
async def create_project(workspace_id: str, body: ProjectCreateRequest):
    session = await get_session()
    try:
        ws = await session.get(Workspace, workspace_id)
        if ws is None:
            raise HTTPException(status_code=404, detail="Workspace not found")
        project = Project(
            id=str(uuid4()),
            workspace_id=workspace_id,
            name=body.name,
            description=body.description,
        )
        session.add(project)
        await session.flush()
        await session.commit()
        return {
            "id": project.id,
            "workspace_id": project.workspace_id,
            "name": project.name,
            "description": project.description,
        }
    finally:
        await session.close()


@router.get("/projects/{project_id}/sites")
async def list_sites(project_id: str):
    session = await get_session()
    try:
        project = await session.get(Project, project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        result = await session.execute(
            select(Site).where(Site.project_id == project_id).order_by(Site.created_at.asc())
        )
        rows = result.scalars().all()
        return [
            {
                "id": s.id,
                "address": s.address,
                "parcel_id": s.parcel_id,
            }
            for s in rows
        ]
    finally:
        await session.close()


@router.post("/projects/{project_id}/sites")
async def create_site(project_id: str, body: SiteCreateRequest):
    session = await get_session()
    try:
        project = await session.get(Project, project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        site = Site(
            id=str(uuid4()),
            workspace_id=project.workspace_id,
            project_id=project_id,
            address=body.address,
            parcel_id=body.parcel_id,
        )
        session.add(site)
        await session.flush()
        await session.commit()
        return {
            "id": site.id,
            "project_id": site.project_id,
            "workspace_id": site.workspace_id,
            "address": site.address,
            "parcel_id": site.parcel_id,
        }
    finally:
        await session.close()
