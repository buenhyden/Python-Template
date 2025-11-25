from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def health_check_test():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
