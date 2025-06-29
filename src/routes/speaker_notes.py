from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import ProjectsAdapter, SpeakerNotesAdapter, get_db
from src.types.speaker_notes import QandA, SpeakerNoteSection

router = APIRouter(prefix="/projects/{project_id}/speaker-notes", tags=["Content"])


class SpeakerNotesResponse(BaseModel):
    id: UUID
    sections: list[SpeakerNoteSection] | None
    talking_points: list[str] | None
    q_and_a: list[QandA] | None
    generated_at: str
    updated_at: str

    @classmethod
    def from_orm(cls, notes):
        sections = None
        if notes.sections:
            sections = [SpeakerNoteSection(**section) for section in notes.sections]

        q_and_a = None
        if notes.q_and_a:
            q_and_a = [QandA(**qa) for qa in notes.q_and_a]

        return cls(
            id=notes.id,
            sections=sections,
            talking_points=notes.talking_points,
            q_and_a=q_and_a,
            generated_at=notes.generated_at.isoformat(),
            updated_at=notes.updated_at.isoformat(),
        )


class SpeakerNotesUpdate(BaseModel):
    sections: list[SpeakerNoteSection] | None = None
    talking_points: list[str] | None = None


@router.get("/", response_model=SpeakerNotesResponse)
def get_speaker_notes(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Get speaker notes"""
    projects_adapter = ProjectsAdapter(db)
    notes_adapter = SpeakerNotesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    notes = notes_adapter.get_speaker_notes(project_id)
    if not notes:
        raise HTTPException(status_code=404, detail="Speaker notes not yet generated")

    return SpeakerNotesResponse.from_orm(notes)


@router.patch("/", response_model=SpeakerNotesResponse)
def update_speaker_notes(
    project_id: UUID,
    request: SpeakerNotesUpdate,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Update speaker notes"""
    projects_adapter = ProjectsAdapter(db)
    notes_adapter = SpeakerNotesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    sections_data = None
    if request.sections:
        sections_data = [section.model_dump() for section in request.sections]

    notes = notes_adapter.update_speaker_notes(
        project_id=project_id,
        sections=sections_data,
        talking_points=request.talking_points,
    )

    if not notes:
        raise HTTPException(status_code=404, detail="Speaker notes not found")

    return SpeakerNotesResponse.from_orm(notes)
