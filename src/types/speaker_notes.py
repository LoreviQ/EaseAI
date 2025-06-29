from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class QandA(BaseModel):
    question: str
    suggested_answer: str
    follow_up_questions: Optional[List[str]]


class SpeakerNoteSection(BaseModel):
    slide_number: int
    detailed_notes: str
    key_points: Optional[List[str]]
    timing_notes: Optional[str]
    transition_notes: Optional[str]


class SpeakerNotes(BaseModel):
    id: UUID
    project_id: UUID
    sections: Optional[List[SpeakerNoteSection]]
    talking_points: Optional[List[str]]
    q_and_a: Optional[List[QandA]]
    generated_at: datetime
    updated_at: datetime
