from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class SlideOutline(BaseModel):
    slide_number: int
    title: str
    content_summary: str
    slide_type: str
    estimated_time: int


class PresentationPlan(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    objective: Optional[str]
    target_audience: Optional[str]
    tone: Optional[str]
    duration: Optional[int]
    outline: Optional[List[SlideOutline]]
    key_messages: Optional[List[str]]
    research_summary: Optional[str]
    created_at: datetime
    updated_at: datetime
