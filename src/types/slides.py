from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class SlideOutline(BaseModel):
    slide_number: int
    title: str
    description: str
    time_spent_on_slide: int


class Slide(SlideOutline):
    content: str


class Slides(BaseModel):
    id: UUID
    project_id: UUID
    slides: Optional[List[Slide]]
    template_id: Optional[str]
    generated_at: datetime
    updated_at: datetime
