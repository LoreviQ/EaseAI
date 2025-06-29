from typing import Any, Dict, List
from uuid import UUID

from pydantic import BaseModel

from src.types import Message, ProjectPhase


class WorkflowState(BaseModel):
    project_id: UUID
    phase: ProjectPhase = ProjectPhase.PREPARATION
    messages: List[Message]
    system_prompt: str
    context: Dict[str, Any]
    generation_config: Dict[str, Any] = {}
