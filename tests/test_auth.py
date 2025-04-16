from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", json={
        "name": "Andrea",
        "email": "andrea@example.com",
        "password": "123456",
        "company": "AutoOpsTestCo"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_login_user():
    response = client.post("/auth/login", json={
        "email": "andrea@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
