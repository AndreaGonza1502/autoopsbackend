from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_webhook_receipt():
    payload = {
        "event": "invitee.created",
        "payload": {
            "invitee": {
                "name": "Test User",
                "email": "test@example.com",
                "start_time": "2025-03-23T10:00:00Z"
            },
            "event": {
                "name": "Reunión AutoOps"
            }
        }
    }

    response = client.post("/webhooks/calendly", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
