"""Main entry point for EaseAI."""

import logging

logger = logging.getLogger("easeai")


def main() -> None:
    """Main function demonstrating the logger."""
    logger.info("Hello, World! EaseAI is starting up...")
    logger.debug("Debug message example")
    logger.warning("Warning message example")
    logger.error("Error message example")
    logger.info("EaseAI initialization complete!")
