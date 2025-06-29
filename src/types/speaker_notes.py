from pydantic import BaseModel


class QandA(BaseModel):
    question: str
    suggested_answer: str
    follow_up_questions: list[str] | None


class SpeakerNoteSection(BaseModel):
    slide_number: int
    detailed_notes: str
    key_points: list[str] | None
    timing_notes: str | None
    transition_notes: str | None
