from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import DeliveryTutorialAdapter, ProjectsAdapter, get_db
from src.types.delivery_tutorial import (
    DeliveryTechnique,
    PracticeExercise,
    TroubleshootingTip,
)

router = APIRouter(prefix="/projects/{project_id}/tutorial", tags=["Content"])


class DeliveryTutorialResponse(BaseModel):
    id: UUID
    introduction: str | None
    preparation_tips: list[str] | None
    delivery_techniques: list[DeliveryTechnique] | None
    practice_exercises: list[PracticeExercise] | None
    troubleshooting: list[TroubleshootingTip] | None
    generated_at: str
    updated_at: str

    @classmethod
    def from_domain(cls, tutorial: Any) -> "DeliveryTutorialResponse":
        return cls(
            id=tutorial.id,
            introduction=tutorial.introduction,
            preparation_tips=tutorial.preparation_tips,
            delivery_techniques=tutorial.delivery_techniques,
            practice_exercises=tutorial.practice_exercises,
            troubleshooting=tutorial.troubleshooting,
            generated_at=tutorial.generated_at.isoformat(),
            updated_at=tutorial.updated_at.isoformat(),
        )


class DeliveryTutorialUpdate(BaseModel):
    introduction: str | None = None
    preparation_tips: list[str] | None = None
    delivery_techniques: list[DeliveryTechnique] | None = None


@router.get("/", response_model=DeliveryTutorialResponse)
def get_delivery_tutorial(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> DeliveryTutorialResponse:
    """Get delivery tutorial"""
    projects_adapter = ProjectsAdapter(db)
    tutorial_adapter = DeliveryTutorialAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    tutorial = tutorial_adapter.get_delivery_tutorial(project_id)
    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not yet generated")

    return DeliveryTutorialResponse.from_domain(tutorial)


@router.patch("/", response_model=DeliveryTutorialResponse)
def update_delivery_tutorial(
    project_id: UUID,
    request: DeliveryTutorialUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> DeliveryTutorialResponse:
    """Update delivery tutorial"""
    projects_adapter = ProjectsAdapter(db)
    tutorial_adapter = DeliveryTutorialAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    techniques_data = None
    if request.delivery_techniques:
        techniques_data = [
            technique.model_dump() for technique in request.delivery_techniques
        ]

    tutorial = tutorial_adapter.update_delivery_tutorial(
        project_id=project_id,
        introduction=request.introduction,
        preparation_tips=request.preparation_tips,
        delivery_techniques=techniques_data,
    )

    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial not found")

    return DeliveryTutorialResponse.from_domain(tutorial)
