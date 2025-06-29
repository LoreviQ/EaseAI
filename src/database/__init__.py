import logging
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .delivery_tutorial_adapter import DeliveryTutorialAdapter
from .messages_adapter import MessagesAdapter
from .presentation_plan_adapter import PresentationPlanAdapter
from .projects_adapter import ProjectsAdapter
from .slides_adapter import SlidesAdapter
from .speaker_notes_adapter import SpeakerNotesAdapter
from .sql_models import Base

__all__ = [
    "Base",
    "DeliveryTutorialAdapter",
    "MessagesAdapter",
    "PresentationPlanAdapter",
    "ProjectsAdapter",
    "SlidesAdapter",
    "SpeakerNotesAdapter",
    "create_tables",
    "get_db_session",
    "get_db",
    "engine",
    "SessionLocal",
]

logger = logging.getLogger("easeai")

DATABASE_URL = os.getenv("DB_CONNECTION_STRING")
if not DATABASE_URL:
    raise ValueError(
        "Database connection string is not set in the environment variables."
    )

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300, echo=False)
logger.info(f"Connected to database at {DATABASE_URL}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    with get_db_session() as session:
        yield session
