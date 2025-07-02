from typing import List, Optional

from pydantic import BaseModel


class SlideOutline(BaseModel):
    slide_number: int
    title: str
    content_summary: str
    estimated_time: int


class PresentationPlan(BaseModel):
    title: str
    objective: Optional[str]
    target_audience: Optional[str]
    tone: Optional[str]
    duration: Optional[int]
    outline: Optional[List[SlideOutline]]
    key_messages: Optional[List[str]]
    research_summary: Optional[str]
