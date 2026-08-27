# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "OK - RELOADED LIVE"

def test_read_items():
    response = client.get("/items/")
    assert response.status_code == 200
