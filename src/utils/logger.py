"""
Logger utility for PresentAI with colorlog support
"""

import logging
import sys

# Try to import colorlog for colored output
try:
    import colorlog

    HAS_COLORLOG = True
except ImportError:
    HAS_COLORLOG = False


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with colored output if colorlog is available

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Don't add handlers if already configured
    if logger.handlers:
        return logger

    logger.setLevel(level)

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    if HAS_COLORLOG:
        # Use colorlog for colored output
        formatter = colorlog.ColoredFormatter(
            "[%(asctime)s] [%(name)s] [%(log_color)s%(levelname)s%(reset)s] %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )
    else:
        # Fallback to standard formatter with level shown
        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Prevent propagation to root logger
    logger.propagate = False

    return logger


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Get a logger instance with the standard PresentAI formatting

    Args:
        name: Logger name (usually __name__)
        level: Logging level

    Returns:
        Configured logger instance
    """
    return setup_logger(name, level)


# Create a default logger for the utils module
logger = get_logger(__name__)
