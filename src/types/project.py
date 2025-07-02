from datetime import datetime
from enum import Enum
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class ProjectPhase(str, Enum):
    PREPARATION = "preparation"
    GENERATION = "generation"
    REVIEW = "review"
    COMPLETE = "complete"


class Project(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    phase: ProjectPhase
    created_at: datetime
    updated_at: datetime
    project_metadata: Optional[Dict]
