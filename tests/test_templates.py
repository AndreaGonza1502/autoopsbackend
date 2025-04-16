from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_template():
    response = client.post(
        "/templates",
        headers={"Authorization": "Bearer faketoken123"},
        json={
            "name": "Plantilla de prueba",
            "type": "task",
            "content": "{\"title\":\"Tarea auto\"}"
        }
    )
    assert response.status_code in [200, 201]
    assert response.json()["name"] == "Plantilla de prueba"

def test_get_templates():
    response = client.get("/templates", headers={"Authorization": "Bearer faketoken123"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
