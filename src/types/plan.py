from typing import Optional

from pydantic import BaseModel, Field


class PresentationPlan(BaseModel):
    title: Optional[str] = Field(
        description="The title of the presentation. Suggest a title based on topic.",
        default=None,
    )
    objective: Optional[str] = Field(
        description="The objective of the presentation", default=None
    )
    target_audience: Optional[str] = Field(
        description="The target audience of the presentation", default=None
    )
    tone: Optional[str] = Field(
        description="The tone of the presentation", default=None
    )
    duration: Optional[str] = Field(
        description="The duration of the presentation", default=None
    )
    research_summary: Optional[str] = Field(
        description="The research summary of the presentation", default=None
    )
