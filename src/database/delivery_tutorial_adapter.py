from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from .sql_models import DeliveryTutorialORM


class DeliveryTutorialAdapter:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_delivery_tutorial(self, project_id: UUID) -> Optional[DeliveryTutorialORM]:
        return (
            self.session.query(DeliveryTutorialORM)
            .filter(DeliveryTutorialORM.project_id == project_id)
            .first()
        )

    def update_delivery_tutorial(
        self,
        project_id: UUID,
        introduction: Optional[str] = None,
        preparation_tips: Optional[list] = None,
        delivery_techniques: Optional[list] = None,
        practice_exercises: Optional[list] = None,
        troubleshooting: Optional[list] = None,
    ) -> Optional[DeliveryTutorialORM]:
        tutorial = self.get_delivery_tutorial(project_id)
        if not tutorial:
            return None

        if introduction is not None:
            tutorial.introduction = introduction
        if preparation_tips is not None:
            tutorial.preparation_tips = preparation_tips
        if delivery_techniques is not None:
            tutorial.delivery_techniques = delivery_techniques
        if practice_exercises is not None:
            tutorial.practice_exercises = practice_exercises
        if troubleshooting is not None:
            tutorial.troubleshooting = troubleshooting

        tutorial.updated_at = datetime.now(timezone.utc)
        self.session.flush()
        return tutorial

    def delivery_tutorial_exists(self, project_id: UUID) -> bool:
        return (
            self.session.query(DeliveryTutorialORM)
            .filter(DeliveryTutorialORM.project_id == project_id)
            .first()
            is not None
        )
