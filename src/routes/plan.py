from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import PresentationPlanAdapter, ProjectsAdapter, get_db
from src.types.plan import SlideOutline

router = APIRouter(prefix="/projects/{project_id}/plan", tags=["Plan"])


class PresentationPlanResponse(BaseModel):
    id: UUID
    title: str
    objective: str | None
    target_audience: str | None
    tone: str | None
    duration: int | None
    outline: list[SlideOutline] | None
    key_messages: list[str] | None
    research_summary: str | None
    created_at: str
    updated_at: str

    @classmethod
    def from_orm(cls, plan):
        outline = None
        if plan.outline:
            outline = [SlideOutline(**item) for item in plan.outline]

        return cls(
            id=plan.id,
            title=plan.title,
            objective=plan.objective,
            target_audience=plan.target_audience,
            tone=plan.tone,
            duration=plan.duration,
            outline=outline,
            key_messages=plan.key_messages,
            research_summary=plan.research_summary,
            created_at=plan.created_at.isoformat(),
            updated_at=plan.updated_at.isoformat(),
        )


class PresentationPlanUpdate(BaseModel):
    title: str | None = None
    objective: str | None = None
    target_audience: str | None = None
    tone: str | None = None
    duration: int | None = None
    outline: list[SlideOutline] | None = None
    key_messages: list[str] | None = None


@router.get("/", response_model=PresentationPlanResponse)
def get_presentation_plan(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Get presentation plan"""
    projects_adapter = ProjectsAdapter(db)
    plan_adapter = PresentationPlanAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    plan = plan_adapter.get_plan(project_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not yet generated")

    return PresentationPlanResponse.from_orm(plan)


@router.patch("/", response_model=PresentationPlanResponse)
def update_presentation_plan(
    project_id: UUID,
    request: PresentationPlanUpdate,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Update presentation plan"""
    projects_adapter = ProjectsAdapter(db)
    plan_adapter = PresentationPlanAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    outline_data = None
    if request.outline:
        outline_data = [outline.model_dump() for outline in request.outline]

    plan = plan_adapter.update_plan(
        project_id=project_id,
        title=request.title,
        objective=request.objective,
        target_audience=request.target_audience,
        tone=request.tone,
        duration=request.duration,
        outline=outline_data,
        key_messages=request.key_messages,
    )

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return PresentationPlanResponse.from_orm(plan)


@router.post("/approve", response_model=dict)
def approve_plan(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)] = None,
):
    """Approve plan and move to content production"""
    projects_adapter = ProjectsAdapter(db)
    plan_adapter = PresentationPlanAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    if not plan_adapter.plan_exists(project_id):
        raise HTTPException(status_code=404, detail="Plan not found")

    raise HTTPException(
        status_code=501, detail="Plan approval functionality not yet implemented"
    )
