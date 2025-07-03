from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.agents import agent
from src.database import (
    MessagesAdapter,
    PresentationPlanAdapter,
    ProjectsAdapter,
    get_db,
)
from src.types import ProjectPhase

router = APIRouter(prefix="/projects/{project_id}/plan", tags=["Plan"])


class PresentationPlanResponse(BaseModel):
    id: UUID
    title: str
    objective: str | None
    target_audience: str | None
    tone: str | None
    duration: int | None
    research_summary: str | None
    created_at: str
    updated_at: str

    @classmethod
    def from_domain(cls, plan: Any) -> "PresentationPlanResponse":
        return cls(
            id=plan.id,
            title=plan.title,
            objective=plan.objective,
            target_audience=plan.target_audience,
            tone=plan.tone,
            duration=plan.duration,
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
    research_summary: str | None = None


@router.get("/", response_model=PresentationPlanResponse)
def get_presentation_plan(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> PresentationPlanResponse:
    """Get presentation plan"""
    projects_adapter = ProjectsAdapter(db)
    plan_adapter = PresentationPlanAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    plan = plan_adapter.get_plan(project_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not yet generated")

    return PresentationPlanResponse.from_domain(plan)


@router.patch("/", response_model=PresentationPlanResponse)
def update_presentation_plan(
    project_id: UUID,
    request: PresentationPlanUpdate,
    db: Annotated[Session, Depends(get_db)],
) -> PresentationPlanResponse:
    """Update presentation plan"""
    projects_adapter = ProjectsAdapter(db)
    plan_adapter = PresentationPlanAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    plan = plan_adapter.update_plan(
        project_id=project_id,
        title=request.title,
        objective=request.objective,
        target_audience=request.target_audience,
        tone=request.tone,
        duration=request.duration,
        research_summary=request.research_summary,
    )

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return PresentationPlanResponse.from_domain(plan)


class ApprovalResponse(BaseModel):
    response: str


@router.post("/approve", response_model=ApprovalResponse)
def approve_plan(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> ApprovalResponse:
    """Approve plan and move to content production"""
    projects_adapter = ProjectsAdapter(db)
    plan_adapter = PresentationPlanAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    if not plan_adapter.plan_exists(project_id):
        raise HTTPException(status_code=404, detail="Plan not found")

    # Approve plan
    projects_adapter.update_project(
        project_id=project_id,
        phase=ProjectPhase.GENERATION,
    )

    messages_adapter = MessagesAdapter(db)
    messages = messages_adapter.get_messages(project_id=project_id)[0]
    initial_state = {
        "messages": [message.AnyMessage for message in messages],
        "project_phase": ProjectPhase.GENERATION,
        "presentation_plan": plan_adapter.get_plan(project_id),
    }
    config = RunnableConfig(
        configurable={
            "project_id": project_id,
            "db_session": db,
        }
    )
    output_state = agent.invoke(initial_state, config=config)

    return ApprovalResponse(response=output_state["messages"][-1].content)
