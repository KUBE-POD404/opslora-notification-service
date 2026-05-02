from fastapi.testclient import TestClient

from app.main import app


def test_notification_health_routes():
    client = TestClient(app)

    response = client.get("/api/v1/notification/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    legacy_response = client.get("/api/notification/health")
    assert legacy_response.status_code == 200
    assert legacy_response.json() == {"status": "ok"}
