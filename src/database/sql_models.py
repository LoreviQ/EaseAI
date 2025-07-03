# mypy: disable-error-code="arg-type,attr-defined,valid-type,misc"

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.types.document import Document, ProcessingStatus
from src.types.message import Message, MessageType
from src.types.plan import PresentationPlan
from src.types.project import Project, ProjectPhase
from src.types.slides import Slide, Slides

Base = declarative_base()


class ProjectORM(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    phase = Column(String(50), default=ProjectPhase.PREPARATION)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    project_metadata = Column(JSON)

    # Relationships
    messages = relationship(
        "MessageORM", back_populates="project", cascade="all, delete-orphan"
    )
    documents = relationship(
        "DocumentORM", back_populates="project", cascade="all, delete-orphan"
    )
    plan = relationship(
        "PresentationPlanORM",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )
    slides = relationship(
        "SlideORM",
        back_populates="project",
        cascade="all, delete-orphan",
    )

    @classmethod
    def from_domain(cls, project: Project) -> "ProjectORM":
        return cls(
            id=project.id,
            title=project.title,
            description=project.description,
            phase=project.phase.value,
            created_at=project.created_at,
            updated_at=project.updated_at,
            project_metadata=project.project_metadata,
        )

    @property
    def domain(self) -> Project:
        return Project(
            id=self.id,
            title=self.title,
            description=self.description,
            phase=ProjectPhase(self.phase),
            created_at=self.created_at,
            updated_at=self.updated_at,
            project_metadata=self.project_metadata,
        )


class MessageORM(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    attachments = Column(JSON)

    # Relationships
    project = relationship("ProjectORM", back_populates="messages")

    @classmethod
    def from_domain(cls, message: Message) -> "MessageORM":
        return cls(
            id=message.id,
            project_id=message.project_id,
            role=message.type.value,
            content=message.content,
            timestamp=message.timestamp,
            attachments=message.attachments,
        )

    @property
    def domain(self) -> Message:
        return Message(
            id=self.id,
            project_id=self.project_id,
            type=MessageType(self.role),
            content=self.content,
            timestamp=self.timestamp,
            attachments=self.attachments,
        )


class DocumentORM(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    file_type = Column(String(50))
    file_size = Column(Integer)
    upload_date = Column(DateTime, default=datetime.now(timezone.utc))
    processing_status = Column(String(20), default=ProcessingStatus.PENDING)
    file_path = Column(String(500))

    # Relationships
    project = relationship("ProjectORM", back_populates="documents")

    @classmethod
    def from_domain(cls, document: Document) -> "DocumentORM":
        return cls(
            id=document.id,
            project_id=document.project_id,
            name=document.name,
            description=document.description,
            file_type=document.file_type,
            file_size=document.file_size,
            upload_date=document.upload_date,
            processing_status=document.processing_status.value,
            file_path=document.file_path,
        )

    @property
    def domain(self) -> Document:
        return Document(
            id=self.id,
            project_id=self.project_id,
            name=self.name,
            description=self.description,
            file_type=self.file_type,
            file_size=self.file_size,
            upload_date=self.upload_date,
            processing_status=ProcessingStatus(self.processing_status),
            file_path=self.file_path,
        )


class PresentationPlanORM(Base):
    __tablename__ = "presentation_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    objective = Column(Text)
    target_audience = Column(String(255))
    tone = Column(String(255))
    duration = Column(String(255))
    research_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    project = relationship("ProjectORM", back_populates="plan")

    @classmethod
    def from_domain(cls, plan: PresentationPlan) -> "PresentationPlanORM":
        return cls(
            title=plan.title,
            objective=plan.objective,
            target_audience=plan.target_audience,
            tone=plan.tone,
            duration=plan.duration,
            research_summary=plan.research_summary,
        )

    @property
    def domain(self) -> PresentationPlan:
        return PresentationPlan(
            title=self.title,
            objective=self.objective,
            target_audience=self.target_audience,
            tone=self.tone,
            duration=self.duration,
            research_summary=self.research_summary,
        )


class SlideORM(Base):
    __tablename__ = "slides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    title = Column(String(255))
    description = Column(Text)
    time_spent_on_slide = Column(Integer)
    slide_number = Column(Integer)
    content = Column(Text)
    speaker_notes = Column(Text)
    delivery_tutorial = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    project = relationship("ProjectORM", back_populates="slides")

    @classmethod
    def from_domain(cls, slide: Slide) -> "SlideORM":
        return cls(
            title=slide.title,
            description=slide.description,
            time_spent_on_slide=slide.time_spent_on_slide,
            slide_number=slide.slide_number,
            content=slide.content,
            speaker_notes=slide.speaker_notes,
            delivery_tutorial=slide.delivery_tutorial,
        )

    @property
    def domain(self) -> Slide:
        return Slide(
            title=self.title,
            description=self.description,
            time_spent_on_slide=self.time_spent_on_slide,
            slide_number=self.slide_number,
            content=self.content,
            speaker_notes=self.speaker_notes,
            delivery_tutorial=self.delivery_tutorial,
        )


