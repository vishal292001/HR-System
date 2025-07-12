import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.models import EmployeeStatus

# Try this approach if the regular TestClient doesn't work
@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["message"] == "Server is up and Running!"

def test_employee_search_valid_org(client):
    response = client.get("/api/employees/search?organization_id=1")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

def test_employee_search_with_filters(client):
    response = client.get("/api/employees/search?organization_id=1&department=Engineering")
    assert response.status_code == 200
    data = response.json()["data"]
    for emp in data:
        assert emp["department"] == "Engineering"

def test_employee_search_status_enum(client):
    response = client.get(f"/api/employees/search?organization_id=1&status={EmployeeStatus.ACTIVE}")
    assert response.status_code == 200

def test_employee_search_invalid_org(client):
    response = client.get("/api/employees/search?organization_id=9999")
    assert response.status_code == 200
    assert response.json()["data"] == []

def test_employee_search_missing_org_id(client):
    response = client.get("/api/employees/search")
    assert response.status_code == 422  # Unprocessable Entity due to missing required param