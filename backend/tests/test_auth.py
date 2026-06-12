def test_register_user(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new@example.com",
            "password": "password123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["full_name"] == "New User"


def test_register_duplicate_email(client):
    payload = {
        "email": "dup@example.com",
        "password": "password123",
        "full_name": "User",
    }
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123",
            "full_name": "Login User",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "wrong@example.com",
            "password": "password123",
            "full_name": "User",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_get_profile(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


def test_update_profile(client, auth_headers):
    response = client.put(
        "/api/v1/auth/me",
        headers=auth_headers,
        json={
            "skills": ["python", "fastapi"],
            "preferred_locations": ["Remote", "NYC"],
            "expected_salary": 120000,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["skills"] == ["python", "fastapi"]
    assert data["expected_salary"] == 120000


def test_password_reset_request(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "reset@example.com",
            "password": "password123",
            "full_name": "Reset User",
        },
    )
    response = client.post(
        "/api/v1/auth/password-reset",
        json={"email": "reset@example.com"},
    )
    assert response.status_code == 200
    assert "reset_token" in response.json()


def test_unauthorized_access(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
