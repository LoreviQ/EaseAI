from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import ProjectsAdapter, SlidesAdapter, get_db
from src.types.slides import Slide

router = APIRouter(prefix="/projects/{project_id}/slides", tags=["Content"])


class SlidesResponse(BaseModel):
    id: UUID
    slides: list[Slide] | None
    template_id: str | None
    generated_at: str
    updated_at: str

    @classmethod
    def from_domain(cls, slides_domain):
        slides_data = None
        if slides_domain.slides:
            slides_data = slides_domain.slides

        return cls(
            id=slides_domain.id,
            slides=slides_data,
            template_id=slides_domain.template_id,
            generated_at=slides_domain.generated_at.isoformat(),
            updated_at=slides_domain.updated_at.isoformat(),
        )


class SlidesUpdate(BaseModel):
    slides: list[dict] | None = None


class RegenerateRequest(BaseModel):
    instructions: str | None = None


@router.get("/", response_model=SlidesResponse)
def get_slides(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Get presentation slides"""
    projects_adapter = ProjectsAdapter(db)
    slides_adapter = SlidesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    slides = slides_adapter.get_slides(project_id)
    if not slides:
        raise HTTPException(status_code=404, detail="Slides not yet generated")

    return SlidesResponse.from_domain(slides)


@router.patch("/", response_model=SlidesResponse)
def update_slides(
    project_id: UUID,
    request: SlidesUpdate,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Update slides content"""
    projects_adapter = ProjectsAdapter(db)
    slides_adapter = SlidesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    slides = slides_adapter.update_slides(
        project_id=project_id,
        slides_data=request.slides,
    )

    if not slides:
        raise HTTPException(status_code=404, detail="Slides not found")

    return SlidesResponse.from_domain(slides)


@router.post("/regenerate", response_model=SlidesResponse)
def regenerate_slides(
    project_id: UUID,
    request: RegenerateRequest | None = None,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Regenerate slides based on plan changes"""
    projects_adapter = ProjectsAdapter(db)
    slides_adapter = SlidesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    if not slides_adapter.slides_exist(project_id):
        raise HTTPException(status_code=404, detail="Slides not found")

    raise HTTPException(
        status_code=501, detail="Slides regeneration functionality not yet implemented"
    )
