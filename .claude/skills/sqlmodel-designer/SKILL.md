---
name: sqlmodel-designer
description: Design database schemas and relationships using SQLModel. Use this skill when defining database models, creating table relationships, setting up database constraints, or designing data structures for FastAPI applications with SQLModel ORM.
---

# SQLModel Designer

Create well-designed database schemas using SQLModel.

## SQLModel Basics

SQLModel combines SQLAlchemy and Pydantic, providing:
- Database models (tables)
- Data validation
- Type safety
- Automatic API schema generation

## Model Creation Workflow

1. Define the table model class
2. Add field types and constraints
3. Set up relationships (if needed)
4. Create database tables
5. Use with FastAPI endpoints

## Basic Model Structure

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: str = Field(default="pending", regex="^(pending|completed)$")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
```

## Field Types and Constraints

### Common Field Types

```python
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class Example(SQLModel, table=True):
    # Integers
    id: Optional[int] = Field(default=None, primary_key=True)
    count: int = Field(default=0, ge=0)  # >= 0

    # Strings
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(regex=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    optional_text: Optional[str] = None

    # Decimals (for money)
    price: Decimal = Field(max_digits=10, decimal_places=2)

    # Booleans
    is_active: bool = Field(default=True)

    # Dates and Times
    created_date: date = Field(default_factory=date.today)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### Field Constraints

```python
from sqlmodel import Field

# Primary key
id: Optional[int] = Field(default=None, primary_key=True)

# Unique constraint
email: str = Field(unique=True)

# Not null (no Optional)
required_field: str

# Nullable (with Optional)
optional_field: Optional[str] = None

# Default value
status: str = Field(default="pending")

# Index for faster queries
username: str = Field(index=True)

# Length constraints
title: str = Field(min_length=1, max_length=200)

# Numeric constraints
age: int = Field(ge=0, le=150)  # greater/less than or equal
price: float = Field(gt=0)  # greater than

# Regex pattern
phone: str = Field(regex=r"^\+?1?\d{9,15}$")
```

## Relationships

### One-to-Many

```python
from typing import Optional, List
from sqlmodel import Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    # Foreign key
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

### Many-to-Many

```python
class TaskTagLink(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    tags: List["Tag"] = Relationship(
        back_populates="tasks", link_model=TaskTagLink
    )

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    tasks: List[Task] = Relationship(
        back_populates="tags", link_model=TaskTagLink
    )
```

## Database Setup

### Engine and Session

```python
from sqlmodel import SQLModel, create_engine, Session

# SQLite database
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

# Create all tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Get session
def get_session():
    with Session(engine) as session:
        yield session
```

### With FastAPI

```python
from fastapi import FastAPI, Depends
from sqlmodel import Session
from typing import Annotated

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

SessionDep = Annotated[Session, Depends(get_session)]

@app.post("/tasks/")
def create_task(task: TaskCreate, session: SessionDep):
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

## CRUD Operations

### Create

```python
def create_task(session: Session, task: TaskCreate) -> Task:
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### Read

```python
from sqlmodel import select

def get_task(session: Session, task_id: int) -> Optional[Task]:
    return session.get(Task, task_id)

def get_all_tasks(session: Session, skip: int = 0, limit: int = 100) -> List[Task]:
    statement = select(Task).offset(skip).limit(limit)
    return session.exec(statement).all()

def get_tasks_by_status(session: Session, status: str) -> List[Task]:
    statement = select(Task).where(Task.status == status)
    return session.exec(statement).all()
```

### Update

```python
def update_task(session: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    db_task = session.get(Task, task_id)
    if not db_task:
        return None

    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

### Delete

```python
def delete_task(session: Session, task_id: int) -> bool:
    db_task = session.get(Task, task_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True
```

## Best Practices

1. **Use Optional for nullable fields** - Clear intent
2. **Set proper constraints** - Data integrity at database level
3. **Add indexes on frequently queried fields** - Better performance
4. **Use datetime.utcnow for timestamps** - Consistent timezone handling
5. **Validate data with Field constraints** - Catch errors early
6. **Use table=True for database models** - Distinguishes from Pydantic schemas
7. **Keep models focused** - One table per class
8. **Use relationships wisely** - Only when needed, can impact performance
9. **Name foreign keys clearly** - user_id, not just id
10. **Use sessions properly** - Always commit or rollback

## Common Patterns

### Base Timestamp Model

```python
from datetime import datetime
from typing import Optional

class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
```

### Soft Delete

```python
class Task(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    deleted_at: Optional[datetime] = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
```

### Enum Fields

```python
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
```
