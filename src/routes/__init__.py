"""Routes module for FastAPI application."""

from .diagnostics import router as diagnostics_router
from .projects import router as projects_router

__all__ = ["diagnostics_router", "projects_router"]
