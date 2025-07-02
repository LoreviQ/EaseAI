from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    description: Optional[str]
    file_type: Optional[str]
    file_size: Optional[int]
    upload_date: datetime
    processing_status: ProcessingStatus
    file_path: Optional[str]
