from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from pydantic import BaseModel


class Project(BaseModel):
    id: UUID
    title: str
    description: Optional[str]
    phase: str
    created_at: datetime
    updated_at: datetime
    project_metadata: Optional[Dict]
