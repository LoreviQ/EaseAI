# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

EaseAI is an AI-powered presentation creation assistant built with Python, managed by UV, and using LangGraph for AI agent functionality.

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
- **FastAPI**: API dependency
- **SQLAlchemy**: Database ORM tool
- **Alembic**: Database migration management

## Project Structure

```
src/app.py            # FastAPI Entrypoint
src/database/         # Database module
src/routes/           # FastAPI Routers
src/types/            # Type definitions
src/utils/            # Utility modules
tests/                # Test suite
```

## Architecture Notes
- Entry point is `uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload`
- Use the 'easeai' logger (logger = logging.getLogger("easeai"))
- Run mypy to check for type issues after generating code