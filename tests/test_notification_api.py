from fastapi.testclient import TestClient

from app.main import app


def test_notification_health_routes():
    client = TestClient(app)

    response = client.get("/api/v1/notification/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

    assert client.get("/api/v1/notification/live").json() == {"status": "ok"}
    assert client.get("/api/v1/notification/startup").json() == {"status": "ok"}

    ready_response = client.get("/api/v1/notification/ready")
    assert ready_response.status_code == 200
    assert ready_response.json() == {
        "status": "ready",
        "checks": {
            "rabbitmq_config": "ok",
            "smtp_config": "ok",
        },
    }

    legacy_response = client.get("/api/notification/health")
    assert legacy_response.status_code == 200
    assert legacy_response.json() == {"status": "ok"}
