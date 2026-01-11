"""Main FastAPI application."""

from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import tasks

app = FastAPI(
    title="Task Management API",
    description="A simple task management API built with FastAPI and SQLModel using TDD",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """Initialize database tables on startup."""
    create_db_and_tables()


# Include routers
app.include_router(tasks.router)


@app.get("/", tags=["root"])
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Task Management API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
