from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.types import PresentationPlan

from .sql_models import PresentationPlanORM


class PresentationPlanAdapter:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_plan(self, project_id: UUID) -> Optional[PresentationPlan]:
        plan = (
            self.session.query(PresentationPlanORM)
            .filter(PresentationPlanORM.project_id == project_id)
            .first()
        )
        return plan.domain if plan else None

    def update_plan(
        self,
        project_id: UUID,
        title: Optional[str] = None,
        objective: Optional[str] = None,
        target_audience: Optional[str] = None,
        tone: Optional[str] = None,
        duration: Optional[int] = None,
        outline: Optional[list] = None,
        key_messages: Optional[list] = None,
    ) -> Optional[PresentationPlan]:
        plan = (
            self.session.query(PresentationPlanORM)
            .filter(PresentationPlanORM.project_id == project_id)
            .first()
        )
        if not plan:
            return None

        if title is not None:
            plan.title = title
        if objective is not None:
            plan.objective = objective
        if target_audience is not None:
            plan.target_audience = target_audience
        if tone is not None:
            plan.tone = tone
        if duration is not None:
            plan.duration = duration
        if outline is not None:
            plan.outline = outline
        if key_messages is not None:
            plan.key_messages = key_messages

        plan.updated_at = datetime.now(timezone.utc)
        self.session.flush()
        return plan.domain

    def plan_exists(self, project_id: UUID) -> bool:
        return (
            self.session.query(PresentationPlanORM)
            .filter(PresentationPlanORM.project_id == project_id)
            .first()
            is not None
        )
