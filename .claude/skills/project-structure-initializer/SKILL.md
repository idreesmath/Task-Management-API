---
name: project-structure-initializer
description: Bootstrap Python project structure with best practices. Use this skill when starting a new Python project, setting up a FastAPI application, or organizing a codebase with proper folder structure, configuration files, and dependency management using UV package manager.
---

# Project Structure Initializer

Set up Python projects with clean, production-ready structure.

## Standard FastAPI Project Structure

```
project-name/
├── .gitignore
├── pyproject.toml          # UV/pip dependencies
├── README.md
├── CLAUDE.md              # Project documentation for AI agents
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app instance
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database setup
│   ├── models/            # SQLModel database models
│   │   ├── __init__.py
│   │   └── task.py
│   ├── routers/           # API route handlers
│   │   ├── __init__.py
│   │   └── tasks.py
│   └── schemas/           # Pydantic schemas (optional, if separate from models)
│       ├── __init__.py
│       └── task.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py        # pytest fixtures
│   └── test_tasks.py
└── .venv/                 # Virtual environment (created by UV)
```

## Setup Workflow

1. **Create project directory**
2. **Initialize UV project**
3. **Create folder structure**
4. **Set up configuration files**
5. **Install dependencies**
6. **Create initial files**

## UV Package Manager

### Initialize Project

```bash
# Create new project
uv init project-name
cd project-name

# Or initialize in existing directory
uv init
```

### Add Dependencies

```bash
# Add production dependencies
uv add fastapi
uv add "uvicorn[standard]"
uv add sqlmodel

# Add development dependencies
uv add --dev pytest
uv add --dev pytest-cov
uv add --dev httpx  # For testing FastAPI
```

### pyproject.toml Structure

```toml
[project]
name = "task-management-api"
version = "0.1.0"
description = "Task Management API with FastAPI and SQLModel"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "sqlmodel>=0.0.22",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-cov>=6.0.0",
    "httpx>=0.28.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --cov=app --cov-report=term-missing"
```

## Essential Files

### .gitignore

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environment
.venv/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.env.local

# Testing
.coverage
htmlcov/
.pytest_cache/

# OS
.DS_Store
Thumbs.db
```

### app/main.py

```python
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import tasks

app = FastAPI(
    title="Task Management API",
    description="API for managing tasks",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Management API"}
```

### app/database.py

```python
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### app/config.py

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Task Management API"
    database_url: str = "sqlite:///./database.db"
    debug: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

### tests/conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

## Running Commands

### Development Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload

# Or with custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=app --cov-report=term-missing

# Specific test file
pytest tests/test_tasks.py

# Verbose output
pytest -v
```

### UV Commands

```bash
# Install all dependencies
uv sync

# Add dependency
uv add package-name

# Add dev dependency
uv add --dev package-name

# Remove dependency
uv remove package-name

# Update dependencies
uv sync --upgrade

# Run command in virtual environment
uv run python script.py
uv run pytest

# Activate virtual environment
# On Windows
.venv\Scripts\activate
# On Unix/MacOS
source .venv/bin/activate
```

## Environment Variables

### .env File

```env
# Application
APP_NAME="Task Management API"
DEBUG=True

# Database
DATABASE_URL=sqlite:///./database.db

# API
API_V1_PREFIX=/api/v1
```

### Load in config.py

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str
    debug: bool = False
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Best Practices

1. **Use UV for dependency management** - Fast, reliable, modern
2. **Separate concerns** - Models, routers, schemas in different files
3. **Use environment variables** - Never hardcode secrets
4. **Write tests from the start** - Set up test infrastructure early
5. **Use .gitignore** - Don't commit generated files or secrets
6. **Document with README** - Clear setup and run instructions
7. **Use CLAUDE.md** - Document for AI agents working on the project
8. **Keep main.py minimal** - Just app setup and router registration
9. **Use dependency injection** - For database sessions, config, etc.
10. **Structure for scalability** - Even small projects benefit from good structure
