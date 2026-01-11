# Task Management API

A modern, production-ready Task Management API built with **FastAPI**, **SQLModel**, and **pytest** using **Test-Driven Development (TDD)**.

## Features

- Full CRUD operations for tasks
- RESTful API design
- Type-safe with Pydantic validation
- SQLite database with SQLModel ORM
- Comprehensive test suite (96% coverage)
- Automatic API documentation (OpenAPI/Swagger)
- Built using TDD methodology

## Technologies Used

### FastAPI
Modern, fast web framework for building APIs with automatic documentation and type safety.

### SQLModel
SQL database ORM that combines SQLAlchemy and Pydantic for seamless database and API integration.

### pytest
Powerful testing framework for ensuring code quality and reliability.

### UV
Fast, modern Python package manager for dependency management.

## Project Structure

```
Task-Management-API/
├── .claude/
│   └── skills/                              # Reusable AI agent skills
│       ├── tdd-api-builder/                 # TDD workflow guidance
│       ├── fastapi-endpoint-generator/      # FastAPI endpoint patterns
│       ├── sqlmodel-designer/               # Database schema design
│       ├── project-structure-initializer/   # Project setup automation
│       ├── code-quality-reviewer/           # Code review guidance
│       └── skill-creator/                   # Skill creation guide
├── app/
│   ├── models/                              # Database models
│   │   ├── __init__.py
│   │   └── task.py
│   ├── routers/                             # API endpoints
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── __init__.py
│   ├── main.py                              # FastAPI app
│   └── database.py                          # Database config
├── tests/
│   ├── __init__.py
│   ├── conftest.py                          # Test fixtures
│   └── test_tasks.py                        # API tests
├── .gitignore                               # Git ignore rules
├── .python-version                          # Python version
├── pyproject.toml                           # Project dependencies
├── uv.lock                                  # Dependency lock file
├── README.md                                # This file
└── CLAUDE.md                                # AI agent documentation
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- UV package manager

### Installation

1. **Install UV** (if not already installed):
   ```bash
   # Windows (PowerShell)
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

   # Linux/macOS
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**:
   ```bash
   cd Task-Management-API

   # Install dependencies
   uv sync
   ```

### Running the API

```bash
# Start the development server
uvicorn app.main:app --reload

# Or with custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

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

## API Endpoints

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks` | List all tasks (with pagination) |
| `GET` | `/tasks/{id}` | Get a specific task |
| `PUT` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |

### Task Model

```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the task management API",
  "status": "pending",
  "created_at": "2026-01-11T10:30:00"
}
```

**Fields:**
- `id` (int): Auto-generated unique identifier
- `title` (string, required): Task title (1-200 characters)
- `description` (string, optional): Task description (max 1000 characters)
- `status` (string): Either "pending" or "completed" (default: "pending")
- `created_at` (datetime): Auto-generated timestamp

## Example Usage

### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn FastAPI",
    "description": "Complete the FastAPI tutorial",
    "status": "pending"
  }'
```

### Get All Tasks

```bash
curl "http://localhost:8000/tasks"
```

### Update a Task

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed"
  }'
```

### Delete a Task

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## AI Agent Skills

This project includes 5 reusable AI agent skills in `.claude/skills/`:

**Technical Skills:**
1. **tdd-api-builder** - TDD workflow for API development
2. **fastapi-endpoint-generator** - FastAPI endpoint patterns
3. **sqlmodel-designer** - Database schema design

**Workflow Skills:**
4. **project-structure-initializer** - Project setup automation
5. **code-quality-reviewer** - Code review and quality checks

These skills can be reused in future projects for faster development.

## Development

### Adding New Features

1. Write tests first (TDD approach)
2. Run tests to see them fail
3. Implement the feature
4. Run tests to see them pass
5. Refactor if needed
6. Commit

### Code Quality

- Type hints on all functions
- Comprehensive test coverage
- Clear error messages
- Proper HTTP status codes
- Input validation with Pydantic

## License

This is a learning project. Feel free to use and modify as needed.

## Contributing

1. Follow TDD methodology
2. Maintain test coverage above 90%
3. Use type hints
4. Follow existing code style
5. Update documentation

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [UV Documentation](https://docs.astral.sh/uv/)