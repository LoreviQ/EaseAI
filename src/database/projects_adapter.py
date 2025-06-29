from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.types import ProjectPhase

from .sql_models import ProjectORM


class ProjectsAdapter:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_project(
        self,
        title: str,
        description: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> ProjectORM:
        project = ProjectORM(
            title=title,
            description=description,
            phase=ProjectPhase.PREPARATION,
            project_metadata=metadata or {},
        )
        self.session.add(project)
        self.session.flush()
        return project

    def get_project(self, project_id: UUID) -> Optional[ProjectORM]:
        return (
            self.session.query(ProjectORM).filter(ProjectORM.id == project_id).first()
        )

    def get_projects(
        self, limit: int = 20, offset: int = 0
    ) -> tuple[List[ProjectORM], int]:
        query = self.session.query(ProjectORM)

        total = query.count()
        projects = (
            query.order_by(ProjectORM.updated_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return projects, total

    def update_project(
        self,
        project_id: UUID,
        title: Optional[str] = None,
        description: Optional[str] = None,
        phase: Optional[ProjectPhase] = None,
        metadata: Optional[dict] = None,
    ) -> Optional[ProjectORM]:
        project = self.get_project(project_id)
        if not project:
            return None

        if title is not None:
            project.title = title
        if description is not None:
            project.description = description
        if phase is not None:
            project.phase = phase
        if metadata is not None:
            project.project_metadata = metadata

        project.updated_at = datetime.now(timezone.utc)
        self.session.flush()
        return project

    def delete_project(self, project_id: UUID) -> bool:
        project = self.get_project(project_id)
        if not project:
            return False

        self.session.delete(project)
        self.session.flush()
        return True

    def project_exists(self, project_id: UUID) -> bool:
        return (
            self.session.query(ProjectORM).filter(ProjectORM.id == project_id).first()
            is not None
        )
