# EaseAI

AI-powered presentation creation assistant that helps users create comprehensive presentations through intelligent research, planning, and content generation.

## Overview

EaseAI is designed to streamline the presentation creation process by providing an AI agent that understands your needs, researches relevant content, and produces professional presentation materials.

### Vision

The project aims to transform how presentations are created by providing:

1. **Intelligent Research**: Interactive conversation to understand presentation goals, audience, and requirements
2. **Smart Planning**: AI-generated presentation plans with optimal structure and content strategy  
3. **Complete Deliverables**: Production of slides, speaker notes, and delivery guidance

## Quick Start

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd EaseAI

# Install dependencies
uv sync --dev
```

### Running

```bash
# Run the hello world demo
uv run python main.py
```

## Development

### Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v
```

### Code Quality

```bash
# Type checking
uv run mypy src/

# Linting and formatting
uv run ruff check
uv run ruff format
```

## Technology Stack

- **Python 3.11+** - Core language
- **UV** - Package and environment management
- **LangGraph** - AI agent workflow framework
- **colorlog** - Enhanced logging
- **pytest** - Testing framework
- **mypy** - Type checking
- **ruff** - Code formatting and linting

## Project Status

Currently in initial development phase with basic project structure, logging, and testing infrastructure in place. The AI agent functionality and presentation generation features are planned for future development.