from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import ProjectsAdapter, get_db

router = APIRouter(prefix="/projects/{project_id}/documents", tags=["Documents"])


class DocumentResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    file_type: str | None
    file_size: int | None
    upload_date: str
    processing_status: str


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    file: UploadFile = File(...),
    name: str | None = Form(None),
    description: str | None = Form(None),
) -> DocumentResponse:
    """Upload research document"""
    projects_adapter = ProjectsAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    raise HTTPException(
        status_code=501, detail="Document upload functionality not yet implemented"
    )


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> list[DocumentResponse]:
    """List project documents"""
    projects_adapter = ProjectsAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    raise HTTPException(
        status_code=501, detail="Document listing functionality not yet implemented"
    )


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    project_id: UUID,
    document_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> DocumentResponse:
    """Get document details"""
    projects_adapter = ProjectsAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    raise HTTPException(
        status_code=501, detail="Document retrieval functionality not yet implemented"
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    project_id: UUID,
    document_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> None:
    """Delete document"""
    projects_adapter = ProjectsAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    raise HTTPException(
        status_code=501, detail="Document deletion functionality not yet implemented"
    )
