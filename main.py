"""Entry point script for EaseAI."""

import logging

from src.easeai.logger import setup_logger
from src.easeai.main import main

if __name__ == "__main__":
    setup_logger("easeai", logging.DEBUG)

    main()
