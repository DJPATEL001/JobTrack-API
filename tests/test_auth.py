from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "testuser123",
            "email": "testuser123@gmail.com",
            "password": "Test@123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["message"] == "User registered successfully"
    assert "user_id" in data


def test_login_user(client):
    # Register user first
    register_response = client.post(
        "/auth/register",
        json={
            "username": "loginuser",
            "email": "loginuser@gmail.com",
            "password": "Test@123"
        }
    )

    assert register_response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": "loginuser",
            "password": "Test@123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user(client):
    # Register user
    client.post(
        "/auth/register",
        json={
            "username": "meuser",
            "email": "meuser@gmail.com",
            "password": "Test@123"
        }
    )

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "meuser",
            "password": "Test@123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "meuser"
    assert data["email"] == "meuser@gmail.com"


def test_protected_route_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_protected_route_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    assert response.status_code == 401


def test_register_duplicate_username(client):
    client.post(
        "/auth/register",
        json={
            "username": "duplicate_user",
            "email": "first@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "duplicate_user",
            "email": "second@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400

def test_register_duplicate_email(client):
    client.post(
        "/auth/register",
        json={
            "username": "email_user_1",
            "email": "same@example.com",
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/register",
        json={
            "username": "email_user_2",
            "email": "same@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 400