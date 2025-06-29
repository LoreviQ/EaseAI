"""Routes module for FastAPI application."""

from fastapi import APIRouter

from .delivery_tutorial import router as delivery_tutorial_router
from .diagnostics import router as diagnostics_router
from .documents import router as documents_router
from .messages import router as messages_router
from .plan import router as plan_router
from .projects import router as projects_router
from .slides import router as slides_router
from .speaker_notes import router as speaker_notes_router

v1 = APIRouter(prefix="/v1")
v1.include_router(delivery_tutorial_router)
v1.include_router(diagnostics_router)
v1.include_router(documents_router)
v1.include_router(messages_router)
v1.include_router(plan_router)
v1.include_router(projects_router)
v1.include_router(slides_router)
v1.include_router(speaker_notes_router)

__all__ = ["v1"]
