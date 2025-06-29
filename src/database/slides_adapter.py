from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from .sql_models import SlidesORM


class SlidesAdapter:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_slides(self, project_id: UUID) -> Optional[SlidesORM]:
        return (
            self.session.query(SlidesORM)
            .filter(SlidesORM.project_id == project_id)
            .first()
        )

    def update_slides(
        self,
        project_id: UUID,
        slides_data: Optional[list] = None,
        template_id: Optional[str] = None,
    ) -> Optional[SlidesORM]:
        slides = self.get_slides(project_id)
        if not slides:
            return None

        if slides_data is not None:
            slides.slides_data = slides_data
        if template_id is not None:
            slides.template_id = template_id

        slides.updated_at = datetime.now(timezone.utc)
        self.session.flush()
        return slides

    def slides_exist(self, project_id: UUID) -> bool:
        return (
            self.session.query(SlidesORM)
            .filter(SlidesORM.project_id == project_id)
            .first()
            is not None
        )
