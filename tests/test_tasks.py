"""Tests for task endpoints following TDD approach."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


class TestCreateTask:
    """Tests for POST /tasks endpoint."""

    def test_create_task_success(self, client: TestClient):
        """Test creating a task with valid data."""
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending"
        }
        response = client.post("/tasks", json=task_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "id" in data
        assert "created_at" in data

    def test_create_task_minimal(self, client: TestClient):
        """Test creating a task with only required fields."""
        task_data = {"title": "Minimal Task"}
        response = client.post("/tasks", json=task_data)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["status"] == "pending"  # Default value
        assert data["description"] is None

    def test_create_task_empty_title(self, client: TestClient):
        """Test creating a task with empty title returns error."""
        task_data = {"title": ""}
        response = client.post("/tasks", json=task_data)

        assert response.status_code == 422

    def test_create_task_missing_title(self, client: TestClient):
        """Test creating a task without title returns error."""
        task_data = {"description": "No title"}
        response = client.post("/tasks", json=task_data)

        assert response.status_code == 422

    def test_create_task_invalid_status(self, client: TestClient):
        """Test creating a task with invalid status returns error."""
        task_data = {
            "title": "Test Task",
            "status": "invalid_status"
        }
        response = client.post("/tasks", json=task_data)

        assert response.status_code == 422


class TestListTasks:
    """Tests for GET /tasks endpoint."""

    def test_list_tasks_empty(self, client: TestClient):
        """Test listing tasks when database is empty."""
        response = client.get("/tasks")

        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_with_data(self, client: TestClient):
        """Test listing tasks returns all tasks."""
        # Create test tasks
        task1 = {"title": "Task 1"}
        task2 = {"title": "Task 2"}
        client.post("/tasks", json=task1)
        client.post("/tasks", json=task2)

        response = client.get("/tasks")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"

    def test_list_tasks_pagination(self, client: TestClient):
        """Test listing tasks with pagination parameters."""
        # Create multiple tasks
        for i in range(5):
            client.post("/tasks", json={"title": f"Task {i}"})

        response = client.get("/tasks?skip=1&limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"


class TestGetTask:
    """Tests for GET /tasks/{task_id} endpoint."""

    def test_get_task_success(self, client: TestClient):
        """Test getting a task by ID."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "Test Task"})
        task_id = create_response.json()["id"]

        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"

    def test_get_task_not_found(self, client: TestClient):
        """Test getting a non-existent task returns 404."""
        response = client.get("/tasks/999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUpdateTask:
    """Tests for PUT /tasks/{task_id} endpoint."""

    def test_update_task_success(self, client: TestClient):
        """Test updating a task with valid data."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "Original Title"})
        task_id = create_response.json()["id"]

        # Update the task
        update_data = {
            "title": "Updated Title",
            "description": "Updated description",
            "status": "completed"
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated description"
        assert data["status"] == "completed"

    def test_update_task_partial(self, client: TestClient):
        """Test partially updating a task."""
        # Create a task
        create_response = client.post("/tasks", json={
            "title": "Original Title",
            "description": "Original description"
        })
        task_id = create_response.json()["id"]

        # Update only title
        update_data = {"title": "New Title"}
        response = client.put(f"/tasks/{task_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title"
        assert data["description"] == "Original description"

    def test_update_task_not_found(self, client: TestClient):
        """Test updating a non-existent task returns 404."""
        update_data = {"title": "Updated Title"}
        response = client.put("/tasks/999", json=update_data)

        assert response.status_code == 404

    def test_update_task_invalid_status(self, client: TestClient):
        """Test updating a task with invalid status returns error."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "Test Task"})
        task_id = create_response.json()["id"]

        # Update with invalid status
        update_data = {"status": "invalid"}
        response = client.put(f"/tasks/{task_id}", json=update_data)

        assert response.status_code == 422


class TestDeleteTask:
    """Tests for DELETE /tasks/{task_id} endpoint."""

    def test_delete_task_success(self, client: TestClient):
        """Test deleting a task."""
        # Create a task
        create_response = client.post("/tasks", json={"title": "Task to Delete"})
        task_id = create_response.json()["id"]

        # Delete the task
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 204

        # Verify task is deleted
        get_response = client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient):
        """Test deleting a non-existent task returns 404."""
        response = client.delete("/tasks/999")

        assert response.status_code == 404


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns welcome message."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
