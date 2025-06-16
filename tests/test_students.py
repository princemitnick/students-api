# tests/test_students.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_students():
    response = client.get("/students")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3