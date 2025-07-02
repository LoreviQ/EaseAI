from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage
from pydantic import BaseModel


class MessageType(str, Enum):
    USER = "user"
    AI = "ai"


class Message(BaseModel):
    id: UUID
    project_id: UUID
    type: MessageType
    content: str
    timestamp: datetime
    attachments: Optional[List]

    @property
    def AnyMessage(self) -> AnyMessage:
        if self.type == MessageType.USER:
            return HumanMessage(content=self.content)
        elif self.type == MessageType.AI:
            return AIMessage(content=self.content)
        else:
            raise ValueError(f"Unknown role: {self.type}")
