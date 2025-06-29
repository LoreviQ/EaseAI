from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from .sql_models import MessageORM


class MessagesAdapter:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_message(
        self,
        project_id: UUID,
        role: str,
        content: str,
        attachments: Optional[list] = None,
    ) -> MessageORM:
        message = MessageORM(
            project_id=project_id,
            role=role,
            content=content,
            attachments=attachments or [],
        )
        self.session.add(message)
        self.session.flush()
        return message

    def get_message(self, message_id: UUID) -> Optional[MessageORM]:
        return (
            self.session.query(MessageORM).filter(MessageORM.id == message_id).first()
        )

    def get_messages(
        self, project_id: UUID, limit: int = 50, offset: int = 0
    ) -> tuple[List[MessageORM], int]:
        query = self.session.query(MessageORM).filter(
            MessageORM.project_id == project_id
        )

        total = query.count()
        messages = (
            query.order_by(MessageORM.timestamp.asc()).offset(offset).limit(limit).all()
        )

        return messages, total

    def delete_message(self, message_id: UUID) -> bool:
        message = self.get_message(message_id)
        if not message:
            return False

        self.session.delete(message)
        self.session.flush()
        return True

    def message_exists(self, message_id: UUID) -> bool:
        return (
            self.session.query(MessageORM).filter(MessageORM.id == message_id).first()
            is not None
        )
