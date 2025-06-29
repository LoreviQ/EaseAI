"""Routes module for FastAPI application."""

from fastapi import APIRouter

from .diagnostics import router as diagnostics_router
from .messages import router as messages_router
from .projects import router as projects_router

v1 = APIRouter(prefix="/v1")
v1.include_router(diagnostics_router)
v1.include_router(messages_router)
v1.include_router(projects_router)

__all__ = ["v1"]
