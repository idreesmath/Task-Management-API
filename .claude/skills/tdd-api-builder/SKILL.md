---
name: tdd-api-builder
description: Build APIs using Test-Driven Development methodology. Use this skill when creating new API endpoints, implementing API features, or refactoring existing APIs. This skill guides through the TDD workflow - writing tests first, then implementing functionality to make tests pass, ensuring code quality and test coverage from the start.
---

# TDD API Builder

Build robust APIs using Test-Driven Development principles.

## TDD Workflow

Follow these steps for every API feature:

1. **Write the test first**
   - Define expected behavior
   - Test success cases
   - Test edge cases and error conditions
   - Run test (should fail initially)

2. **Implement minimum code to pass**
   - Write only enough code to make the test pass
   - Keep it simple
   - Don't add extra features

3. **Refactor if needed**
   - Improve code quality
   - Remove duplication
   - Maintain passing tests

4. **Repeat for next feature**

## Testing Best Practices

### Test Structure

```python
def test_feature_name():
    # Arrange: Set up test data
    test_data = {...}

    # Act: Execute the functionality
    response = client.post("/endpoint", json=test_data)

    # Assert: Verify the results
    assert response.status_code == 200
    assert response.json()["field"] == expected_value
```

### What to Test

**Required tests for each endpoint:**
- Valid input returns expected output
- Invalid input returns appropriate error
- Missing required fields returns validation error
- Database operations work correctly
- Status codes are correct

**Edge cases:**
- Empty strings
- Null values
- Duplicate entries
- Non-existent IDs
- Invalid data types

### pytest Patterns

**Fixtures for setup:**
```python
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_task():
    return {"title": "Test Task", "description": "Test Description"}
```

**Parametrize for multiple cases:**
```python
@pytest.mark.parametrize("status_code,payload", [
    (201, {"title": "Valid", "description": "Valid"}),
    (422, {"title": ""}),  # Missing required field
    (422, {}),  # Empty payload
])
def test_create_task_variations(client, status_code, payload):
    response = client.post("/tasks", json=payload)
    assert response.status_code == status_code
```

## API Testing Checklist

For each endpoint, ensure tests cover:

- [ ] Success path (200/201)
- [ ] Not found (404)
- [ ] Validation errors (422)
- [ ] Server errors (500)
- [ ] Data persistence
- [ ] Response structure
- [ ] Authentication/Authorization (if applicable)

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_tasks.py

# Run specific test
pytest tests/test_tasks.py::test_create_task

# Verbose output
pytest -v
```

## Common Patterns

### Testing CRUD Operations

**Create:**
```python
def test_create_resource(client):
    response = client.post("/resources", json={"name": "test"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test"
    assert "id" in data
```

**Read:**
```python
def test_get_resource(client, created_resource_id):
    response = client.get(f"/resources/{created_resource_id}")
    assert response.status_code == 200
    assert response.json()["id"] == created_resource_id
```

**Update:**
```python
def test_update_resource(client, created_resource_id):
    response = client.put(
        f"/resources/{created_resource_id}",
        json={"name": "updated"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "updated"
```

**Delete:**
```python
def test_delete_resource(client, created_resource_id):
    response = client.delete(f"/resources/{created_resource_id}")
    assert response.status_code == 204

    # Verify it's actually deleted
    response = client.get(f"/resources/{created_resource_id}")
    assert response.status_code == 404
```

## Red-Green-Refactor Cycle

1. **Red**: Write a failing test
2. **Green**: Make it pass with minimal code
3. **Refactor**: Improve the code while keeping tests green

Always commit after reaching green state.