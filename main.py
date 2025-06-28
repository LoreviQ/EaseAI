"""Entry point script for EaseAI."""

import logging

import uvicorn

from easeai.utils.logger import setup_logger

if __name__ == "__main__":
    setup_logger("easeai", logging.DEBUG)
    logger = logging.getLogger("easeai")
    logger.info("EaseAI started on port 8000")
    uvicorn.run(
        "src.easeai.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=None,
    )
