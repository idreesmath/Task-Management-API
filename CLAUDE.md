# Task Management API - Claude Documentation

## Project Overview

This is a **Task Management API** built with **FastAPI**, **SQLModel**, and **pytest** using **Test-Driven Development (TDD)** principles. The project serves as a learning platform for modern Python API development and AI-assisted programming workflows.

## Project Goals

1. **Build a production-ready Task Management API** with full CRUD operations
2. **Learn and apply modern Python technologies** (FastAPI, SQLModel, pytest, UV)
3. **Extract reusable AI agent skills** from repetitive development tasks
4. **Practice Test-Driven Development** methodology
5. **Create skills for AI-native development** workflows

## Technology Stack

### Core Technologies

- **FastAPI** - Modern, fast web framework for building APIs
  - Why: Automatic API documentation, type safety, high performance, easy to test
  - Used for: API endpoints, request/response handling, dependency injection

- **SQLModel** - SQL database ORM combining SQLAlchemy and Pydantic
  - Why: Type safety, data validation, works seamlessly with FastAPI
  - Used for: Database models, CRUD operations, data validation

- **pytest** - Testing framework
  - Why: Simple, powerful, excellent FastAPI integration
  - Used for: Unit tests, integration tests, test fixtures

- **UV** - Fast Python package manager
  - Why: Modern, fast, reliable dependency management
  - Used for: Installing packages, managing virtual environments

### Database

- **SQLite** - Lightweight SQL database
  - Why: Simple, no setup required, perfect for development and learning
  - Used for: Persistent data storage

## Project Structure

```
Task-Management-API/
├── .claude/
│   └── skills/                    # Reusable AI agent skills
│       ├── tdd-api-builder/       # TDD workflow guidance
│       ├── fastapi-endpoint-generator/  # FastAPI endpoint patterns
│       ├── sqlmodel-designer/     # Database schema design
│       ├── project-structure-initializer/  # Project setup
│       └── code-quality-reviewer/ # Code review guidance
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application instance
│   ├── database.py                # Database configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py               # Task SQLModel definition
│   └── routers/
│       ├── __init__.py
│       └── tasks.py              # Task API endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # pytest fixtures and setup
│   └── test_tasks.py             # Task endpoint tests
├── .gitignore
├── pyproject.toml                # UV/Python project config
├── README.md                     # User-facing documentation
└── CLAUDE.md                     # This file - AI agent documentation
```

## API Endpoints

### Tasks Resource

**Base URL:** `/tasks`

| Method | Endpoint | Description | Status Code |
|--------|----------|-------------|-------------|
| POST | `/tasks` | Create a new task | 201 |
| GET | `/tasks` | List all tasks (with pagination) | 200 |
| GET | `/tasks/{id}` | Get a specific task | 200/404 |
| PUT | `/tasks/{id}` | Update a task | 200/404 |
| DELETE | `/tasks/{id}` | Delete a task | 204/404 |

### Task Model

```python
{
    "id": int,              # Auto-generated
    "title": str,           # Required, 1-200 chars
    "description": str,     # Optional, max 1000 chars
    "status": str,          # "pending" or "completed"
    "created_at": datetime  # Auto-generated
}
```

## Development Workflow

### Test-Driven Development Process

1. **Write the test first** - Define expected behavior
2. **Run test (should fail)** - Red phase
3. **Write minimal code to pass** - Green phase
4. **Refactor if needed** - Improve code quality
5. **Commit** - Save progress
6. **Repeat** for next feature

### Skills Usage

This project includes 5 reusable skills that guide development:

**Technical Skills:**
1. **tdd-api-builder** - Use when writing tests and implementing API features
2. **fastapi-endpoint-generator** - Use when creating new API endpoints
3. **sqlmodel-designer** - Use when designing database models

**Workflow Skills:**
4. **project-structure-initializer** - Use when setting up new projects
5. **code-quality-reviewer** - Use before commits and during code review

## Setup Instructions

### Prerequisites

- Python 3.11+
- UV package manager

### Installation

```bash
# Clone repository
cd Task-Management-API

# Install UV (if not already installed)
# On Windows:
# powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Initialize and install dependencies
uv sync

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Unix/MacOS:
source .venv/bin/activate
```

### Running the Application

```bash
# Development server with auto-reload
uvicorn app.main:app --reload

# Or specify host and port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# API documentation available at:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_tasks.py

# Verbose output
pytest -v
```

## Code Standards

### Testing Requirements

- All endpoints must have tests
- Minimum test coverage: success path, error cases, edge cases
- Use pytest fixtures for common setup
- Test database isolation (in-memory SQLite for tests)

### Code Quality

- Type hints on all functions
- Pydantic models for request/response validation
- Proper HTTP status codes
- Clear error messages
- No hardcoded values (use config)
- Single responsibility principle

### Security

- No SQL injection (use SQLModel ORM)
- Input validation with Pydantic
- No hardcoded secrets (use environment variables)
- Proper error handling (don't expose internal details)

## Key Learnings

### Why FastAPI?

- Automatic API documentation (OpenAPI/Swagger)
- Built-in request/response validation
- Dependency injection system
- Excellent performance
- Native async support
- Type hints provide IDE support

### Why SQLModel?

- Combines SQLAlchemy (database) and Pydantic (validation)
- Single model definition for DB and API
- Type safety throughout
- Works seamlessly with FastAPI
- Reduces code duplication

### Why pytest?

- Simple, readable test syntax
- Powerful fixture system
- Great FastAPI integration (TestClient)
- Excellent error reporting
- Coverage reporting

### Why TDD?

- Ensures code is testable from the start
- Documents expected behavior
- Catches bugs early
- Enables confident refactoring
- Forces thinking about edge cases

## Common Tasks

### Add a New Endpoint

1. **Write test first** (in `tests/test_tasks.py`)
2. **Run test** - Should fail
3. **Implement endpoint** (in `app/routers/tasks.py`)
4. **Run test** - Should pass
5. **Refactor if needed**

### Add a New Model Field

1. **Write test** for the new field
2. **Update SQLModel** (in `app/models/task.py`)
3. **Update Pydantic schemas** if separate
4. **Update tests** for existing endpoints
5. **Run all tests**
6. **Delete database.db** (SQLite will recreate with new schema)

### Add a New Resource

1. **Create model** (e.g., `app/models/user.py`)
2. **Create router** (e.g., `app/routers/users.py`)
3. **Create tests** (e.g., `tests/test_users.py`)
4. **Register router** in `app/main.py`
5. **Follow TDD workflow**

## Troubleshooting

### Database Issues

```bash
# Delete database and start fresh
rm database.db

# Or in PowerShell
Remove-Item database.db

# Restart the application - it will recreate tables
```

### Test Issues

```bash
# Clear pytest cache
pytest --cache-clear

# Run with verbose output to see details
pytest -vv

# Run a single test for debugging
pytest tests/test_tasks.py::test_create_task -v
```

### Dependency Issues

```bash
# Re-sync dependencies
uv sync

# Add missing dependency
uv add package-name

# Remove virtual environment and recreate
rm -rf .venv  # Unix/MacOS
Remove-Item -Recurse .venv  # Windows
uv sync
```

## Next Steps

After completing the basic Task Management API:

1. Add user authentication
2. Add task assignment to users
3. Add task priorities and due dates
4. Add filtering and search
5. Add pagination
6. Deploy to production (e.g., Railway, Render, Fly.io)

## Skills for Reuse

The five skills created for this project can be reused in future projects:

1. **tdd-api-builder** - Any API development project
2. **fastapi-endpoint-generator** - FastAPI projects needing CRUD endpoints
3. **sqlmodel-designer** - Projects using SQLModel for database
4. **project-structure-initializer** - Any new Python project
5. **code-quality-reviewer** - Any code review or quality check

These skills encapsulate best practices and repetitive tasks, making future development faster and more consistent.

## Contributing

When working on this project:

1. Always write tests first (TDD)
2. Run tests before committing
3. Use the provided skills for guidance
4. Keep code simple and readable
5. Add comments only when necessary (code should be self-documenting)
6. Update this document when adding new features

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [REST API Best Practices](https://restfulapi.net/)
