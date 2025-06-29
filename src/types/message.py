from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class Message(BaseModel):
    id: UUID
    project_id: UUID
    role: str
    content: str
    timestamp: datetime
    attachments: Optional[List]
