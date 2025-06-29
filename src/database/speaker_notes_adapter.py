# mypy: disable-error-code="assignment"

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.types import SpeakerNotes

from .sql_models import SpeakerNotesORM


class SpeakerNotesAdapter:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_speaker_notes(self, project_id: UUID) -> Optional[SpeakerNotes]:
        notes = (
            self.session.query(SpeakerNotesORM)
            .filter(SpeakerNotesORM.project_id == project_id)
            .first()
        )
        return notes.domain if notes else None

    def update_speaker_notes(
        self,
        project_id: UUID,
        sections: Optional[list] = None,
        talking_points: Optional[list] = None,
        q_and_a: Optional[list] = None,
    ) -> Optional[SpeakerNotes]:
        notes = (
            self.session.query(SpeakerNotesORM)
            .filter(SpeakerNotesORM.project_id == project_id)
            .first()
        )
        if not notes:
            return None

        if sections is not None:
            notes.sections = sections
        if talking_points is not None:
            notes.talking_points = talking_points
        if q_and_a is not None:
            notes.q_and_a = q_and_a

        notes.updated_at = datetime.now(timezone.utc)
        self.session.flush()
        return notes.domain

    def speaker_notes_exist(self, project_id: UUID) -> bool:
        return (
            self.session.query(SpeakerNotesORM)
            .filter(SpeakerNotesORM.project_id == project_id)
            .first()
            is not None
        )
