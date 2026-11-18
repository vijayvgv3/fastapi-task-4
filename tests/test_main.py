from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_employees():
    response = client.get("/employees")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_employee():
    response = client.get("/employees/Arun")
    assert response.status_code == 200
    assert response.json()["name"] == "Arun"


def test_employee_not_found():
    response = client.get("/employees/Unknown")
    assert response.status_code == 404


def test_create_employee():
    response = client.post(
        "/employees",
        json={"name": "Ravi", "salary": 35000}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Ravi"


def test_invalid_salary():
    response = client.post(
        "/employees",
        json={"name": "Test", "salary": 0}
    )
    assert response.status_code == 422