import logging
from typing import Annotated, Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
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
from src.types import PresentationPlan

logger = logging.getLogger("easeai")
router = APIRouter(prefix="/projects/{project_id}/messages", tags=["Research"])


class CreateMessageRequest(BaseModel):
    message: str
    attachments: list[UUID] | None = None


class MessageResponse(BaseModel):
    response: str
    presentation_plan: Optional[PresentationPlan] = None


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def send_message(
    project_id: UUID,
    request: CreateMessageRequest,
    db: Annotated[Session, Depends(get_db)],
) -> MessageResponse:
    """Send message to AI agent"""
    logger.debug(f"Sending message to project {project_id}: {request.message}")
    projects_adapter = ProjectsAdapter(db)
    messages_adapter = MessagesAdapter(db)
    plan_adapter = PresentationPlanAdapter(db)

    project = projects_adapter.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    messages_adapter.create_message(
        project_id=project_id,
        role="user",
        content=request.message,
        attachments=request.attachments,
    )

    # Prepare the agent state and invoke the agent
    messages = messages_adapter.get_messages(project_id=project_id)[0]
    initial_state = {
        "messages": [message.AnyMessage for message in messages],
        "project_phase": project.phase,
        "presentation_plan": plan_adapter.get_plan(project_id),
    }
    config = RunnableConfig(
        configurable={
            "project_id": project_id,
            "db_session": db,
        }
    )
    output_state = agent.invoke(initial_state, config=config)
    response = output_state["messages"][-1]
    if output_state["project_phase"] != initial_state["project_phase"]:
        projects_adapter.update_project(
            project_id=project_id,
            phase=output_state["project_phase"],
        )

    # Log the response
    logger.debug(f"Agent response: {response.content}")

    return MessageResponse(
        response=response.content,
        presentation_plan=output_state.get("presentation_plan"),
    )


@router.get("/", response_model=dict)
def get_conversation_history(
    project_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    """Get conversation history"""
    projects_adapter = ProjectsAdapter(db)
    messages_adapter = MessagesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    messages, total = messages_adapter.get_messages(
        project_id=project_id, limit=limit, offset=offset
    )

    return {
        "messages": messages,
        "total": total,
        "has_more": (offset + limit) < total,
    }
