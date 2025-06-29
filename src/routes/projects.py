from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import ProjectsAdapter, get_db

router = APIRouter(prefix="/projects", tags=["Projects"])


class CreateProjectRequest(BaseModel):
    title: str
    description: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    phase: str
    created_at: str
    updated_at: str
    metadata: dict | None

    @classmethod
    def from_orm(cls, project):
        return cls(
            id=project.id,
            title=project.title,
            description=project.description,
            phase=project.phase,
            created_at=project.created_at.isoformat(),
            updated_at=project.updated_at.isoformat(),
            metadata=project.project_metadata,
        )


class ProjectSummary(BaseModel):
    id: UUID
    title: str
    phase: str
    updated_at: str

    @classmethod
    def from_orm(cls, project):
        return cls(
            id=project.id,
            title=project.title,
            phase=project.phase,
            updated_at=project.updated_at.isoformat(),
        )


class UpdateProjectRequest(BaseModel):
    title: str | None = None
    description: str | None = None


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    request: CreateProjectRequest, db: Annotated[Session, Depends(get_db)]
):
    """Create new presentation project"""
    adapter = ProjectsAdapter(db)

    project = adapter.create_project(
        title=request.title, description=request.description
    )

    return ProjectResponse.from_orm(project)


@router.get("/", response_model=dict)
def get_projects(
    limit: int = 20,
    offset: int = 0,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """List user's projects with pagination"""
    adapter = ProjectsAdapter(db)

    projects, total = adapter.get_projects(limit=limit, offset=offset)

    return {
        "projects": [ProjectSummary.from_orm(project) for project in projects],
        "total": total,
    }


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: UUID, db: Annotated[Session, Depends(get_db)]):
    """Get project details"""
    adapter = ProjectsAdapter(db)

    project = adapter.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse.from_orm(project)


@router.patch("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: UUID,
    request: UpdateProjectRequest,
    db: Annotated[Session, Depends(get_db)],
):
    """Update project metadata"""
    adapter = ProjectsAdapter(db)

    project = adapter.update_project(
        project_id=project_id,
        title=request.title,
        description=request.description,
    )

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectResponse.from_orm(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: UUID, db: Annotated[Session, Depends(get_db)]):
    """Delete project"""
    adapter = ProjectsAdapter(db)

    success = adapter.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
