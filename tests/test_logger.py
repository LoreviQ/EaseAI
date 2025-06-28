"""Tests for the logger module."""

import logging
from unittest.mock import patch

from easeai.logger import setup_logger


def test_setup_logger_creates_logger():
    """Test that setup_logger creates a logger with correct name."""
    logger = setup_logger("test_logger")
    assert logger.name == "test_logger"
    assert isinstance(logger, logging.Logger)


def test_setup_logger_default_name():
    """Test that setup_logger uses default name when none provided."""
    logger = setup_logger()
    assert logger.name == "easeai"


def test_setup_logger_sets_level():
    """Test that setup_logger sets the correct logging level."""
    logger = setup_logger("test", level=logging.DEBUG)
    assert logger.level == logging.DEBUG


def test_setup_logger_with_file():
    """Test that setup_logger can add file handler."""
    with patch("logging.FileHandler") as mock_file_handler:
        logger = setup_logger("test", log_file="test.log")

        # Should have created a file handler
        mock_file_handler.assert_called_once_with("test.log")

        # Should have at least 2 handlers (console + file)
        assert len(logger.handlers) >= 2


def test_setup_logger_idempotent():
    """Test that calling setup_logger multiple times doesn't add duplicate handlers."""
    logger1 = setup_logger("idempotent_test")
    handler_count = len(logger1.handlers)

    logger2 = setup_logger("idempotent_test")

    # Should be the same logger instance
    assert logger1 is logger2
    # Should not have added more handlers
    assert len(logger2.handlers) == handler_count
