from fastapi.testclient import TestClient
from app.main import app, commitments

client = TestClient(app)

def setup_function():
    commitments.clear()

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_commitments():
    response = client.get("/api/commitments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
