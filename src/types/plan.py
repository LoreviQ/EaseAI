from typing import Optional

from pydantic import BaseModel


class PresentationPlan(BaseModel):
    title: Optional[str] = None
    objective: Optional[str] = None
    target_audience: Optional[str] = None
    tone: Optional[str] = None
    duration: Optional[str] = None
    research_summary: Optional[str] = None
