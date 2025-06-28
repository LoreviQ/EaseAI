"""Tests for the main module."""

from unittest.mock import patch

from easeai.main import main


def test_main_function_runs():
    """Test that main function runs without error."""
    # This should not raise any exceptions
    main()


def test_main_function_logs_messages():
    """Test that main function produces expected log messages."""
    with patch("easeai.main.setup_logger") as mock_setup_logger:
        mock_logger = mock_setup_logger.return_value

        main()

        # Verify logger was set up
        mock_setup_logger.assert_called_once()

        # Verify expected log calls were made
        assert mock_logger.info.call_count >= 2
        assert mock_logger.debug.call_count >= 1
        assert mock_logger.warning.call_count >= 1
        assert mock_logger.error.call_count >= 1
