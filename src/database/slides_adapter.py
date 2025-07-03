# mypy: disable-error-code="assignment"

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.types import Slide

from .sql_models import SlideORM


class SlidesAdapter:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_slides(self, project_id: UUID) -> List[Slide]:
        slides = (
            self.session.query(SlideORM)
            .filter(SlideORM.project_id == project_id)
            .order_by(SlideORM.slide_number)
            .all()
        )
        return [slide.domain for slide in slides]

    def get_slide(self, project_id: UUID, slide_number: int) -> Optional[Slide]:
        slide = (
            self.session.query(SlideORM)
            .filter(SlideORM.project_id == project_id)
            .filter(SlideORM.slide_number == slide_number)
            .first()
        )
        return slide.domain if slide else None

    def create_slide(self, project_id: UUID, slide: Slide) -> Slide:
        slide_orm = SlideORM.from_domain(slide)
        slide_orm.project_id = project_id
        self.session.add(slide_orm)
        self.session.flush()
        return slide_orm.domain

    def update_slide(
        self, project_id: UUID, slide_number: int, slide: Slide
    ) -> Optional[Slide]:
        slide_orm = (
            self.session.query(SlideORM)
            .filter(SlideORM.project_id == project_id)
            .filter(SlideORM.slide_number == slide_number)
            .first()
        )
        if not slide_orm:
            return None

        slide_orm.title = slide.title
        slide_orm.description = slide.description
        slide_orm.time_spent_on_slide = slide.time_spent_on_slide
        slide_orm.content = slide.content
        slide_orm.speaker_notes = slide.speaker_notes
        slide_orm.delivery_tutorial = slide.delivery_tutorial
        slide_orm.updated_at = datetime.now(timezone.utc)

        self.session.flush()
        return slide_orm.domain

    def slide_exists(self, project_id: UUID, slide_number: int) -> bool:
        return (
            self.session.query(SlideORM)
            .filter(SlideORM.project_id == project_id)
            .filter(SlideORM.slide_number == slide_number)
            .first()
            is not None
        )

    def delete_slides(self, project_id: UUID) -> None:
        self.session.query(SlideORM).filter(SlideORM.project_id == project_id).delete()
        self.session.flush()
