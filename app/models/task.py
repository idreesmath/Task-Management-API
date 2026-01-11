"""Task model and schemas."""

from datetime import datetime
from typing import Literal, Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator


class Task(SQLModel, table=True):
    """Task database model."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")
    status: str = Field(default="pending", description="Task status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")


class TaskCreate(SQLModel):
    """Schema for creating a new task."""
    title: str = Field(min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description")
    status: Literal["pending", "completed"] = Field(default="pending", description="Task status")


class TaskUpdate(SQLModel):
    """Schema for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[Literal["pending", "completed"]] = Field(default=None)


class TaskResponse(SQLModel):
    """Schema for task responses."""
    id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
