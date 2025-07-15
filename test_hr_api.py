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


def test_employee_search_invalid_status_enum(client):
    response = client.get("/api/employees/search?organization_id=1&status=UNKNOWN")
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "value is not a valid enumeration member; permitted: 'ACTIVE', 'NOT_STARTED', 'TERMINATED'"

def test_employee_search_invalid_limit_value(client):
    response = client.get("/api/employees/search?organization_id=1&limit=1000")  # Limit > 100
    assert response.status_code == 422
    assert any("ensure this value is less than or equal to 100" in err["msg"] for err in response.json()["detail"])

def test_employee_search_invalid_offset_type(client):
    response = client.get("/api/employees/search?organization_id=1&offset=abc")  # Invalid int
    assert response.status_code == 422
    assert any("value is not a valid integer" in err["msg"] for err in response.json()["detail"])

def test_employee_search_empty_string_params(client):
    response = client.get("/api/employees/search?organization_id=1&name=")
    assert response.status_code == 200  # Should still be accepted and treated as no filter
