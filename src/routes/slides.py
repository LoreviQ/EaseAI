from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import ProjectsAdapter, SlidesAdapter, get_db
from src.types.slides import Slide

router = APIRouter(prefix="/projects/{project_id}/slides", tags=["Content"])


class SlidesResponse(BaseModel):
    slides: list[Slide]

    @classmethod
    def from_domain(cls, slides_list: list[Slide]) -> "SlidesResponse":
        return cls(slides=slides_list)


class SlideUpdate(BaseModel):
    slide_number: int
    title: str | None = None
    description: str | None = None
    time_spent_on_slide: int | None = None
    content: str | None = None
    speaker_notes: str | None = None
    delivery_tutorial: str | None = None


class RegenerateRequest(BaseModel):
    instructions: str | None = None


@router.get("/", response_model=SlidesResponse)
def get_slides(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> SlidesResponse:
    """Get presentation slides"""
    projects_adapter = ProjectsAdapter(db)
    slides_adapter = SlidesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    slides = slides_adapter.get_slides(project_id)
    if not slides:
        raise HTTPException(status_code=404, detail="Slides not yet generated")

    return SlidesResponse.from_domain(slides)


@router.patch("/{slide_number}", response_model=Slide)
def update_slide(
    project_id: UUID,
    slide_number: int,
    request: SlideUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> Slide:
    """Update a specific slide"""
    projects_adapter = ProjectsAdapter(db)
    slides_adapter = SlidesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    # Get existing slide
    existing_slide = slides_adapter.get_slide(project_id, slide_number)
    if not existing_slide:
        raise HTTPException(status_code=404, detail="Slide not found")

    # Create updated slide
    updated_slide = Slide(
        title=request.title or existing_slide.title,
        description=request.description or existing_slide.description,
        time_spent_on_slide=request.time_spent_on_slide or existing_slide.time_spent_on_slide,
        slide_number=slide_number,
        content=request.content or existing_slide.content,
        speaker_notes=request.speaker_notes or existing_slide.speaker_notes,
        delivery_tutorial=request.delivery_tutorial or existing_slide.delivery_tutorial,
    )

    result = slides_adapter.update_slide(project_id, slide_number, updated_slide)
    if not result:
        raise HTTPException(status_code=404, detail="Slide not found")

    return result


@router.post("/regenerate", response_model=SlidesResponse)
def regenerate_slides(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    request: RegenerateRequest | None = None,
) -> SlidesResponse:
    """Regenerate slides based on plan changes"""
    projects_adapter = ProjectsAdapter(db)
    slides_adapter = SlidesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    slides = slides_adapter.get_slides(project_id)
    if not slides:
        raise HTTPException(status_code=404, detail="Slides not found")

    raise HTTPException(
        status_code=501, detail="Slides regeneration functionality not yet implemented"
    )
