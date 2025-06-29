from pydantic import BaseModel


class Slide(BaseModel):
    slide_number: int
    title: str
    content: dict
    layout: str | None
    transitions: dict | None
    speaker_cues: list[str] | None
