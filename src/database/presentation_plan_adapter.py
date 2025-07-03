# mypy: disable-error-code="assignment"

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
        plan_patch: PresentationPlan,
    ) -> Optional[PresentationPlan]:
        db_plan = (
            self.session.query(PresentationPlanORM)
            .filter(PresentationPlanORM.project_id == project_id)
            .first()
        )
        if not db_plan:
            db_plan = PresentationPlanORM(
                project_id=project_id,
                title=plan_patch.title,
                objective=plan_patch.objective,
                target_audience=plan_patch.target_audience,
                tone=plan_patch.tone,
                duration=plan_patch.duration,
                research_summary=plan_patch.research_summary,
            )
            self.session.add(db_plan)
            self.session.flush()
            return db_plan.domain

        if plan_patch.title is not None:
            db_plan.title = plan_patch.title
        if plan_patch.objective is not None:
            db_plan.objective = plan_patch.objective
        if plan_patch.target_audience is not None:
            db_plan.target_audience = plan_patch.target_audience
        if plan_patch.tone is not None:
            db_plan.tone = plan_patch.tone
        if plan_patch.duration is not None:
            db_plan.duration = plan_patch.duration
        if plan_patch.research_summary is not None:
            db_plan.research_summary = plan_patch.research_summary

        db_plan.updated_at = datetime.now(timezone.utc)
        self.session.flush()
        return db_plan.domain

    def plan_exists(self, project_id: UUID) -> bool:
        return (
            self.session.query(PresentationPlanORM)
            .filter(PresentationPlanORM.project_id == project_id)
            .first()
            is not None
        )
