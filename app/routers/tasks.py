"""Task API endpoints."""

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models.task import Task, TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate, session: SessionDep):
    """Create a new task.

    Args:
        task: Task data to create
        session: Database session

    Returns:
        Created task

    Raises:
        HTTPException: If validation fails
    """
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.get("/", response_model=List[TaskResponse])
def list_tasks(session: SessionDep, skip: int = 0, limit: int = 100):
    """List all tasks with pagination.

    Args:
        session: Database session
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return

    Returns:
        List of tasks
    """
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, session: SessionDep):
    """Get a specific task by ID.

    Args:
        task_id: ID of the task to retrieve
        session: Database session

    Returns:
        Task data

    Raises:
        HTTPException: If task not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, session: SessionDep):
    """Update an existing task.

    Args:
        task_id: ID of the task to update
        task_update: Updated task data
        session: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: If task not found
    """
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Update only provided fields
    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, session: SessionDep):
    """Delete a task.

    Args:
        task_id: ID of the task to delete
        session: Database session

    Returns:
        None

    Raises:
        HTTPException: If task not found
    """
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    session.delete(task)
    session.commit()
    return None
