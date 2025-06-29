# mypy: disable-error-code="arg-type,attr-defined,valid-type,misc"

import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.types import ProcessingStatus, ProjectPhase
from src.types.delivery_tutorial import (
    DeliveryTechnique,
    DeliveryTutorial,
    PracticeExercise,
    TroubleshootingTip,
)
from src.types.document import Document
from src.types.message import Message
from src.types.plan import PresentationPlan, SlideOutline
from src.types.project import Project
from src.types.slides import Slide, Slides
from src.types.speaker_notes import QandA, SpeakerNotes, SpeakerNoteSection

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
        "SlidesORM",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )
    speaker_notes = relationship(
        "SpeakerNotesORM",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )
    delivery_tutorial = relationship(
        "DeliveryTutorialORM",
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )

    @classmethod
    def from_domain(cls, project: Project) -> "ProjectORM":
        return cls(
            id=project.id,
            title=project.title,
            description=project.description,
            phase=project.phase,
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
            phase=self.phase,
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
            role=message.role,
            content=message.content,
            timestamp=message.timestamp,
            attachments=message.attachments,
        )

    @property
    def domain(self) -> Message:
        return Message(
            id=self.id,
            project_id=self.project_id,
            role=self.role,
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
            processing_status=document.processing_status,
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
            processing_status=self.processing_status,
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
    duration = Column(Integer)
    outline = Column(JSON)
    key_messages = Column(JSON)
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
        outline_data = None
        if plan.outline:
            outline_data = [outline.model_dump() for outline in plan.outline]

        return cls(
            id=plan.id,
            project_id=plan.project_id,
            title=plan.title,
            objective=plan.objective,
            target_audience=plan.target_audience,
            tone=plan.tone,
            duration=plan.duration,
            outline=outline_data,
            key_messages=plan.key_messages,
            research_summary=plan.research_summary,
            created_at=plan.created_at,
            updated_at=plan.updated_at,
        )

    @property
    def domain(self) -> PresentationPlan:
        outline = None
        if self.outline:
            outline = [SlideOutline(**item) for item in self.outline]

        return PresentationPlan(
            id=self.id,
            project_id=self.project_id,
            title=self.title,
            objective=self.objective,
            target_audience=self.target_audience,
            tone=self.tone,
            duration=self.duration,
            outline=outline,
            key_messages=self.key_messages,
            research_summary=self.research_summary,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class SlidesORM(Base):
    __tablename__ = "slides"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    slides_data = Column(JSON)
    template_id = Column(String(100))
    generated_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    project = relationship("ProjectORM", back_populates="slides")

    @classmethod
    def from_domain(cls, slides: Slides) -> "SlidesORM":
        slides_data = None
        if slides.slides:
            slides_data = [slide.model_dump() for slide in slides.slides]

        return cls(
            id=slides.id,
            project_id=slides.project_id,
            slides_data=slides_data,
            template_id=slides.template_id,
            generated_at=slides.generated_at,
            updated_at=slides.updated_at,
        )

    @property
    def domain(self) -> Slides:
        slides_list = None
        if self.slides_data:
            slides_list = [Slide(**slide) for slide in self.slides_data]

        return Slides(
            id=self.id,
            project_id=self.project_id,
            slides=slides_list,
            template_id=self.template_id,
            generated_at=self.generated_at,
            updated_at=self.updated_at,
        )


class SpeakerNotesORM(Base):
    __tablename__ = "speaker_notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    sections = Column(JSON)
    talking_points = Column(JSON)
    q_and_a = Column(JSON)
    generated_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    project = relationship("ProjectORM", back_populates="speaker_notes")

    @classmethod
    def from_domain(cls, speaker_notes: SpeakerNotes) -> "SpeakerNotesORM":
        sections_data = None
        if speaker_notes.sections:
            sections_data = [section.model_dump() for section in speaker_notes.sections]

        q_and_a_data = None
        if speaker_notes.q_and_a:
            q_and_a_data = [qa.model_dump() for qa in speaker_notes.q_and_a]

        return cls(
            id=speaker_notes.id,
            project_id=speaker_notes.project_id,
            sections=sections_data,
            talking_points=speaker_notes.talking_points,
            q_and_a=q_and_a_data,
            generated_at=speaker_notes.generated_at,
            updated_at=speaker_notes.updated_at,
        )

    @property
    def domain(self) -> SpeakerNotes:
        sections = None
        if self.sections:
            sections = [SpeakerNoteSection(**section) for section in self.sections]

        q_and_a = None
        if self.q_and_a:
            q_and_a = [QandA(**qa) for qa in self.q_and_a]

        return SpeakerNotes(
            id=self.id,
            project_id=self.project_id,
            sections=sections,
            talking_points=self.talking_points,
            q_and_a=q_and_a,
            generated_at=self.generated_at,
            updated_at=self.updated_at,
        )


class DeliveryTutorialORM(Base):
    __tablename__ = "delivery_tutorials"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    introduction = Column(Text)
    preparation_tips = Column(JSON)
    delivery_techniques = Column(JSON)
    practice_exercises = Column(JSON)
    troubleshooting = Column(JSON)
    generated_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )

    # Relationships
    project = relationship("ProjectORM", back_populates="delivery_tutorial")

    @classmethod
    def from_domain(cls, delivery_tutorial: DeliveryTutorial) -> "DeliveryTutorialORM":
        techniques_data = None
        if delivery_tutorial.delivery_techniques:
            techniques_data = [
                technique.model_dump()
                for technique in delivery_tutorial.delivery_techniques
            ]

        exercises_data = None
        if delivery_tutorial.practice_exercises:
            exercises_data = [
                exercise.model_dump()
                for exercise in delivery_tutorial.practice_exercises
            ]

        troubleshooting_data = None
        if delivery_tutorial.troubleshooting:
            troubleshooting_data = [
                tip.model_dump() for tip in delivery_tutorial.troubleshooting
            ]

        return cls(
            id=delivery_tutorial.id,
            project_id=delivery_tutorial.project_id,
            introduction=delivery_tutorial.introduction,
            preparation_tips=delivery_tutorial.preparation_tips,
            delivery_techniques=techniques_data,
            practice_exercises=exercises_data,
            troubleshooting=troubleshooting_data,
            generated_at=delivery_tutorial.generated_at,
            updated_at=delivery_tutorial.updated_at,
        )

    @property
    def domain(self) -> DeliveryTutorial:
        techniques = None
        if self.delivery_techniques:
            techniques = [
                DeliveryTechnique(**technique) for technique in self.delivery_techniques
            ]

        exercises = None
        if self.practice_exercises:
            exercises = [
                PracticeExercise(**exercise) for exercise in self.practice_exercises
            ]

        troubleshooting = None
        if self.troubleshooting:
            troubleshooting = [
                TroubleshootingTip(**tip) for tip in self.troubleshooting
            ]

        return DeliveryTutorial(
            id=self.id,
            project_id=self.project_id,
            introduction=self.introduction,
            preparation_tips=self.preparation_tips,
            delivery_techniques=techniques,
            practice_exercises=exercises,
            troubleshooting=troubleshooting,
            generated_at=self.generated_at,
            updated_at=self.updated_at,
        )
