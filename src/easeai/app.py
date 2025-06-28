"""Main entry point for EaseAI."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import diagnostics_router
from .utils.logger import setup_logger

setup_logger("easeai", logging.DEBUG)
logger = logging.getLogger("easeai")

app = FastAPI(
    title="EaseAI API",
    description="AI-powered presentation creation assistant API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnostics_router)
logger.info("Initialized EaseAI API")
