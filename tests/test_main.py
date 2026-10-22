from fastapi.testclient import TestClient
from src.main import app
from datetime import datetime, timedelta, timezone
from jose import jwt
from config.config import SECRET_KEY
import uuid

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_get_tasks_without_token():
    response = client.get("/tasks")
    assert response.status_code == 401

def test_create_user_and_login():
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"

    response = client.post("/users", json={
        "username": unique_username,
        "password": "testpass123",
        "email": f"{unique_username}@test.com"
        })
    assert response.status_code == 200

    response = client.post("/login", data={
        "username": unique_username,
        "password": "testpass123"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]

    response = client.get("/tasks", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200

def test_create_duplicate_user():
    username = f"testuser_{uuid.uuid4().hex[:8]}"

    response = client.post("/users", json={
        "username": username,
        "password": "testpass123",
        "email": f"{username}@test.com"
    })
    assert response.status_code == 200

    response = client.post("/users", json={
        "username": username,
        "password": "testpass123",
        "email": f"{username}@test.com"
    })
    assert response.status_code == 409

def test_expire_token():
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"

    response = client.post("/users", json={
        "username": unique_username,
        "password": "testpass123",
        "email": f"{unique_username}@test.com"
        })
    assert response.status_code == 200

    expire = datetime.now(timezone.utc) - timedelta(minutes=5)

    token = jwt.encode(
        {
            "sub" : unique_username,
            "exp" : expire,
        },
        SECRET_KEY,
        algorithm = "HS256"
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.get(
        "/tasks/",
        headers=headers
    )
    assert response.status_code == 401