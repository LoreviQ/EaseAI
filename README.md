# EaseAI

AI-powered presentation creation assistant that helps users create comprehensive presentations through intelligent research, planning, and content generation.

## Overview

EaseAI is a sophisticated AI agent system that transforms how presentations are created. Through interactive conversation and intelligent workflow orchestration, it guides users from initial concept to polished presentation deliverables.

### Key Features

- **🤖 AI Agent Workflow**: LangGraph-powered multi-phase presentation creation
- **💬 Interactive Research**: Conversational AI that understands your presentation goals
- **📊 Smart Planning**: AI-generated presentation plans with optimal structure
- **🎨 Content Generation**: HTML/CSS/JS slide production with speaker notes
- **🔄 Real-time Collaboration**: Live conversation and content updates
- **📱 Modern Interface**: React-based demo with responsive design

## Architecture

EaseAI consists of a **FastAPI backend** with **LangGraph agent workflows** and a **React frontend demo**:

### Backend Components
- **FastAPI API** - RESTful endpoints with OpenAPI documentation
- **LangGraph Agents** - Multi-node AI workflow orchestration
- **PostgreSQL Database** - Project and conversation persistence
- **Google Gemini AI** - Advanced language model integration

### Frontend Demo
- **React 18** - Modern component-based interface
- **Tailwind CSS** - Responsive, utility-first styling
- **Real-time Updates** - Live conversation and content preview

## Quick Start

### Prerequisites

- Python 3.11 or higher
- UV package manager
- PostgreSQL database
- Google AI API key

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd EaseAI

# Install dependencies
uv sync --dev

# Set up database
docker-compose up -d  # Start PostgreSQL
uv run alembic upgrade head  # Run migrations
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration:
# DATABASE_URL=postgresql://user:password@localhost/easeai
# GOOGLE_AI_API_KEY=your_api_key_here
```

### Running

```bash
# Start the FastAPI server
uv run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# In another terminal, start the React demo
cd demo
npm install
npm start
```

Access the application at `http://localhost:3000`

## API Endpoints

### Project Management
- `POST /v1/projects/` - Create new presentation project
- `GET /v1/projects/` - List all projects with pagination
- `GET /v1/projects/{id}` - Get project details and status
- `PATCH /v1/projects/{id}` - Update project metadata
- `DELETE /v1/projects/{id}` - Delete project

### Interactive Research
- `POST /v1/projects/{id}/messages/` - Send message to AI agent
- `GET /v1/projects/{id}/messages/` - Get conversation history

### Plan Management
- `GET /v1/projects/{id}/plan/` - Get presentation plan
- `PATCH /v1/projects/{id}/plan/` - Update plan details
- `POST /v1/projects/{id}/plan/approve` - Approve plan and start generation

### Content Access
- `GET /v1/projects/{id}/slides/` - Get generated slides
- `PATCH /v1/projects/{id}/slides/{slide_number}` - Update individual slides
- `POST /v1/projects/{id}/slides/regenerate` - Regenerate content

API documentation available at `http://localhost:8000/docs`

## Development

### Database Management

```bash
# Create new migration
uv run alembic revision --autogenerate -m "Description"

# Apply migrations
uv run alembic upgrade head

# Rollback migration
uv run alembic downgrade -1
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_specific.py
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

### Backend
- **Python 3.11+** - Core language with async support
- **FastAPI** - High-performance API framework
- **LangGraph** - AI agent workflow orchestration
- **SQLAlchemy** - Database ORM with async support
- **Alembic** - Database migration management
- **PostgreSQL** - Relational database
- **Google Generative AI** - LLM integration (Gemini 2.5 Flash)
- **Pydantic** - Data validation and type safety

### Frontend
- **React 18** - Modern component framework
- **Tailwind CSS** - Utility-first styling
- **TypeScript** - Type-safe JavaScript

### Development Tools
- **UV** - Fast Python package management
- **MyPy** - Static type checking
- **Ruff** - Code linting and formatting
- **Docker Compose** - Database containerization

## Project Phases

EaseAI guides users through four distinct phases:

1. **Preparation** - Interactive research and goal definition
2. **Generation** - AI-powered content creation
3. **Review** - Content refinement and editing
4. **Complete** - Final presentation delivery

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following the code style guidelines
4. Run tests and type checking (`uv run pytest && uv run mypy src/`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.