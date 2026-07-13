from fastapi.testclient import TestClient


def test_register_user(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "full_name": "New User",
            "password": "securepass123",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == "newuser@example.com"
    assert payload["username"] == "newuser"
    assert "id" in payload


def test_login_user_success(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "loginuser@example.com",
            "username": "loginuser",
            "full_name": "Login User",
            "password": "securepass123",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser@example.com", "password": "securepass123"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
    assert payload["refresh_token"]


def test_login_user_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "missing@example.com", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_refresh_token_success(client: TestClient) -> None:
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "refreshuser@example.com",
            "username": "refreshuser",
            "full_name": "Refresh User",
            "password": "securepass123",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "refreshuser@example.com", "password": "securepass123"},
    )
    refresh_token = login_response.json()["refresh_token"]

    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    payload = response.json()
    assert payload["token_type"] == "bearer"
    assert payload["access_token"]
