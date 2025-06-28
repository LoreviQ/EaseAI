"""Main entry point for EaseAI."""

from easeai.logger import setup_logger


def main() -> None:
    """Main function demonstrating the logger."""
    logger = setup_logger()

    logger.info("Hello, World! EaseAI is starting up...")
    logger.debug("Debug message example")
    logger.warning("Warning message example")
    logger.error("Error message example")
    logger.info("EaseAI initialization complete!")


if __name__ == "__main__":
    main()
