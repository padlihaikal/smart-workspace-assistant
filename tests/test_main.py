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

def get_auth_headers():
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

    return {"Authorization": f"Bearer {token}"}

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

def test_upload_document_without_token():
    response = client.post(
        "/documents",
        files={
            "file": ("a.txt", b"hello world", "text/plain")
        }
    )

    assert response.status_code == 401

def test_upload_document_success():
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

    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/documents",
        files={
            "file": ("a.txt", b"hello world", "text/plain")
        },
        headers=headers
    )

    assert response.status_code == 200
    assert "id" in response.json()
    assert "file_name" in response.json()
    assert "text" not in response.json()

def test_get_document_without_token():
    response = client.get("/documents")
    assert response.status_code == 401

def test_get_document_ownership():
    headers_a = get_auth_headers()
    
    response = client.post(
        "/documents",
        files={
            "file": ("a.txt", b"hello world", "text/plain")
        },
        headers=headers_a
    )

    headers_b = get_auth_headers()
    response = client.get("/documents", headers=headers_b)

    assert response.status_code == 200
    assert response.json() == []

    response = client.get("/documents", headers=headers_a)

    assert response.status_code == 200
    assert response.json()[0]["file_name"] == "a.txt"

def test_get_document_with_id():
    response = client.get("/documents/1")
    assert response.status_code == 401

    headers_a = get_auth_headers()

    response = client.post(
        "/documents",
        files={
            "file": ("a.txt", b"hello world", "text/plain")
        },
        headers=headers_a
    )

    assert response.status_code == 200
    document_id = response.json()["id"]
    
    response = client.get(
        f"/documents/{document_id}",
        headers=headers_a
        )


    assert response.status_code == 200
    assert response.json()["file_name"] == "a.txt"

    headers_b = get_auth_headers()

    response = client.get(
        f"/documents/{document_id}",
        headers=headers_b
    )

    assert response.status_code == 404