from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Document(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    description: Optional[str]
    file_type: Optional[str]
    file_size: Optional[int]
    upload_date: datetime
    processing_status: str
    file_path: Optional[str]
