from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import ProjectsAdapter, get_db

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
