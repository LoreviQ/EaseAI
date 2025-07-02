from datetime import datetime
from typing import List, Optional
from uuid import UUID

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from pydantic import BaseModel


class Message(BaseModel):
    id: UUID
    project_id: UUID
    role: str
    content: str
    timestamp: datetime
    attachments: Optional[List]

    @property
    def AnyMessage(self) -> AnyMessage:
        if self.role == "user":
            return HumanMessage(content=self.content)
        elif self.role == "ai":
            return AIMessage(content=self.content)
        else:
            raise ValueError(f"Unknown role: {self.role}")
