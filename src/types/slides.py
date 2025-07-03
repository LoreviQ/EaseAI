from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel


class SlideOutline(BaseModel):
    slide_number: Optional[int] = None
    title: Optional[str]
    description: Optional[str]
    time_spent_on_slide: Optional[int]


class Slide(SlideOutline):
    content: Optional[str] = None
    speaker_notes: Optional[str] = None
    delivery_tutorial: Optional[str] = None

    def __str__(self) -> str:
        parts = [f"Slide {self.slide_number or 'N/A'}"]
        if self.title:
            parts.append(f"Title: {self.title}")
        if self.description:
            parts.append(f"Description: {self.description}")
        if self.time_spent_on_slide:
            parts.append(f"Time: {self.time_spent_on_slide}s")
        if self.content:
            content_preview = (
                self.content[:100] + "..." if len(self.content) > 100 else self.content
            )
            parts.append(f"Content: {content_preview}")
        if self.speaker_notes:
            parts.append("Speaker Notes: [Generated]")
        if self.delivery_tutorial:
            parts.append("Delivery Tutorial: [Generated]")
        return " | ".join(parts)


class Slides(BaseModel):
    id: UUID
    project_id: UUID
    slides: Optional[List[Slide]]
    template_id: Optional[str]
    generated_at: datetime
    updated_at: datetime


def update_slides(
    existing: Optional[Dict[int, Slide]], new: Dict[int, Slide]
) -> Dict[int, Slide]:
    """Reducer function to update slides dictionary with partial updates"""
    if existing is None:
        return new
    updated = existing.copy()
    for slide_num, slide_update in new.items():
        if slide_num in updated:
            # Merge the existing slide with the update
            existing_slide = updated[slide_num]
            updated_slide = Slide(
                slide_number=slide_update.slide_number or existing_slide.slide_number,
                title=slide_update.title or existing_slide.title,
                description=slide_update.description or existing_slide.description,
                time_spent_on_slide=(
                    slide_update.time_spent_on_slide
                    or existing_slide.time_spent_on_slide
                ),
                content=slide_update.content or existing_slide.content,
                speaker_notes=(
                    slide_update.speaker_notes or existing_slide.speaker_notes
                ),
                delivery_tutorial=(
                    slide_update.delivery_tutorial or existing_slide.delivery_tutorial
                ),
            )
            updated[slide_num] = updated_slide
        else:
            updated[slide_num] = slide_update
    return updated
