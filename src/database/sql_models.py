import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from src.types import ProcessingStatus, ProjectPhase

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
