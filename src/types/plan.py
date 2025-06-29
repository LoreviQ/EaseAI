from pydantic import BaseModel


class SlideOutline(BaseModel):
    slide_number: int
    title: str
    content_summary: str
    slide_type: str
    estimated_time: int
