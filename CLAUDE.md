# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EaseAI is an AI-powered presentation creation assistant built with Python, managed by UV, and using LangChain for AI agent functionality.

### Long-term Vision

The project aims to create an AI agent that helps users create comprehensive presentations through a multi-stage process:

1. **Conversational Research Phase**: The agent interacts with users to understand the presentation's purpose, audience, tone, and length. It researches provided documents and uses web tools to gather relevant information.

2. **Presentation Plan Generation**: Based on the research, the agent creates a detailed presentation plan including tone, length, target audience, and content structure.

3. **Content Production**: The agent executes the plan to produce three key deliverables:
   - **Slides**: Web-based presentation slides (similar to Figma slides format)
   - **Speaker Notes**: Detailed reference information for the presenter
   - **Delivery Tutorial**: Script suggestions and delivery guidance

## Technology Stack

- **Python 3.11+**: Core language
- **UV**: Package and environment management
- **LangGraph**: AI agent workflow framework
- **colorlog**: Custom logging with colored output
- **pytest**: Testing framework
- **mypy**: Type checking
- **ruff**: Linting and code formatting

## Project Structure

```
src/easeai/           # Main package
├── __init__.py       # Package initialization
├── main.py           # Main entry point with hello world demo
└── logger.py         # Custom logger setup with colorlog

tests/                # Test suite
├── test_main.py      # Tests for main module
└── test_logger.py    # Tests for logger module

main.py               # Project entry point script
```

## Development Commands

### Environment Setup
```bash
uv sync                    # Install dependencies
uv sync --dev              # Install with dev dependencies
```

### Running Code
```bash
uv run python main.py      # Run the main entry point
uv run python -m easeai.main  # Run main module directly
```

### Testing
```bash
uv run pytest             # Run all tests
uv run pytest tests/ -v   # Run tests with verbose output
uv run pytest tests/test_main.py  # Run specific test file
```

### Code Quality
```bash
uv run mypy src/          # Type checking
uv run ruff check         # Linting
uv run ruff format        # Code formatting
```

## Logger Configuration

The project uses a custom logger with colorlog that outputs formatted messages:
- Format: `[timestamp] [level] message`
- Colored output for different log levels
- Supports both console and file logging
- Accessible via `from easeai.logger import setup_logger`

## Architecture Notes

- Entry point is through `main.py` which imports from `src.easeai.main`
- Logger is designed to be imported and used throughout the application
- Tests are comprehensive and include mocking for external dependencies
- Type hints are enforced via mypy configuration
- Code style is managed by ruff