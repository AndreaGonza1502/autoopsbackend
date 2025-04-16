from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

FAKE_TOKEN = "Bearer faketoken123"  # reemplazar con fixture real en producción

def test_create_feedback():
    response = client.post(
        "/feedback",
        headers={"Authorization": FAKE_TOKEN},
        json={
            "message": "La IA fue muy útil",
            "response": "Aquí está tu tarea",
            "rating": 5
        }
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert "id" in data
    assert data["rating"] == 5
