"""Health check endpoint."""

from datetime import datetime, timezone
from typing import Dict

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """
    API health check endpoint.

    Returns:
        Dict containing status, timestamp, and version information.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "1.0.0",
    }
