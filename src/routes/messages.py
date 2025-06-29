from typing import Annotated, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.database import MessagesAdapter, ProjectsAdapter, get_db

router = APIRouter(prefix="/projects/{project_id}/messages", tags=["Research"])


class CreateMessageRequest(BaseModel):
    message: str
    attachments: list[UUID] | None = None


class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    timestamp: str
    attachments: list | None

    @classmethod
    def from_domain(cls, message: Any) -> "MessageResponse":
        return cls(
            id=message.id,
            role=message.role,
            content=message.content,
            timestamp=message.timestamp.isoformat(),
            attachments=message.attachments,
        )


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_200_OK)
def send_message(
    project_id: UUID,
    request: CreateMessageRequest,
    db: Annotated[Session, Depends(get_db)],
) -> MessageResponse:
    """Send message to AI agent"""
    projects_adapter = ProjectsAdapter(db)
    messages_adapter = MessagesAdapter(db)

    if not projects_adapter.project_exists(project_id):
        raise HTTPException(status_code=404, detail="Project not found")

    message = messages_adapter.create_message(
        project_id=project_id,
        role="user",
        content=request.message,
        attachments=request.attachments,
    )

    return MessageResponse.from_domain(message)


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
        "messages": [MessageResponse.from_domain(message) for message in messages],
        "total": total,
        "has_more": (offset + limit) < total,
    }
