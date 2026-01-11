---
name: fastapi-endpoint-generator
description: Generate FastAPI CRUD endpoints with proper structure, validation, error handling, and dependency injection. Use this skill when creating new API endpoints for resources, implementing CRUD operations, or setting up RESTful API routes. Ensures consistent API design patterns and best practices.
---

# FastAPI Endpoint Generator

Create well-structured FastAPI endpoints following best practices.

## Endpoint Creation Workflow

1. Define the Pydantic model/schema
2. Create the router
3. Implement endpoints with proper:
   - Type hints
   - Dependency injection
   - Error handling
   - Status codes
   - Response models

## Standard CRUD Endpoints

### Create Resource (POST)

```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/resources", tags=["resources"])

class ResourceCreate(BaseModel):
    name: str
    description: str | None = None

class ResourceResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(resource: ResourceCreate):
    # Database operation
    db_resource = create_db_resource(resource)
    return db_resource
```

### Read Single Resource (GET)

```python
@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int):
    resource = get_db_resource(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found"
        )
    return resource
```

### List Resources (GET)

```python
@router.get("/", response_model=list[ResourceResponse])
async def list_resources(skip: int = 0, limit: int = 100):
    resources = get_all_db_resources(skip=skip, limit=limit)
    return resources
```

### Update Resource (PUT)

```python
class ResourceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

@router.put("/{resource_id}", response_model=ResourceResponse)
async def update_resource(resource_id: int, resource: ResourceUpdate):
    db_resource = get_db_resource(resource_id)
    if not db_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found"
        )

    updated_resource = update_db_resource(resource_id, resource)
    return updated_resource
```

### Delete Resource (DELETE)

```python
@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resource(resource_id: int):
    resource = get_db_resource(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resource with id {resource_id} not found"
        )

    delete_db_resource(resource_id)
    return None
```

## Pydantic Model Patterns

### Base Models

```python
from pydantic import BaseModel, Field
from datetime import datetime

class ResourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)

class ResourceCreate(ResourceBase):
    pass

class ResourceUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)

class ResourceResponse(ResourceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # For SQLModel compatibility
```

## Dependency Injection

### Database Session

```python
from typing import Annotated
from fastapi import Depends
from sqlmodel import Session

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/")
async def create_resource(resource: ResourceCreate, session: SessionDep):
    db_resource = Resource(**resource.model_dump())
    session.add(db_resource)
    session.commit()
    session.refresh(db_resource)
    return db_resource
```

## Error Handling

### Standard HTTP Exceptions

```python
from fastapi import HTTPException, status

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Resource not found"
)

# 422 Validation Error (automatic with Pydantic)
# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid operation"
)

# 409 Conflict
raise HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Resource already exists"
)

# 500 Internal Server Error
raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error"
)
```

## Status Codes

Use appropriate HTTP status codes:

- `200 OK` - Successful GET, PUT
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

## Router Organization

### Project Structure

```
app/
├── main.py
├── routers/
│   ├── __init__.py
│   ├── tasks.py
│   └── users.py
└── models/
    └── task.py
```

### Main App Setup

```python
from fastapi import FastAPI
from app.routers import tasks, users

app = FastAPI(title="My API", version="1.0.0")

app.include_router(tasks.router)
app.include_router(users.router)
```

## Best Practices

1. **Use type hints everywhere** - Enables automatic validation and documentation
2. **Define response models** - Controls what data is returned
3. **Use status code constants** - More readable than numbers
4. **Implement proper error handling** - Return meaningful error messages
5. **Add tags to routers** - Organizes API documentation
6. **Use dependency injection** - Cleaner, testable code
7. **Validate inputs with Pydantic** - Automatic validation and error messages
8. **Keep routers focused** - One resource per router file
