import pytest
from httpx import AsyncClient


async def test_register(client: AsyncClient):
    response = await client.post("/auth/register", json={
        "name": "Alice",
        "email": "alice@test.com",
        "age": 25,
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "alice@test.com"
    assert data["name"] == "Alice"


async def test_register_duplicate_email(client: AsyncClient):
    payload = {
        "name": "Bob",
        "email": "bob@test.com",
        "age": 30,
        "password": "password123"
    }
    await client.post("/auth/register", json=payload)
    response = await client.post("/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


async def test_login_success(client: AsyncClient):
    await client.post("/auth/register", json={
        "name": "Charlie",
        "email": "charlie@test.com",
        "age": 22,
        "password": "password123"
    })
    response = await client.post("/auth/login", json={
        "email": "charlie@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Login successful"
    assert "access_token" in response.cookies


async def test_login_wrong_password(client: AsyncClient):
    await client.post("/auth/register", json={
        "name": "Dave",
        "email": "dave@test.com",
        "age": 28,
        "password": "correctpass"
    })
    response = await client.post("/auth/login", json={
        "email": "dave@test.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


async def test_me_authenticated(auth_client: AsyncClient):
    response = await auth_client.get("/auth/me")
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


async def test_me_unauthenticated(client: AsyncClient):
    response = await client.get("/auth/me")
    assert response.status_code == 401


async def test_logout(auth_client: AsyncClient):
    response = await auth_client.post("/auth/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"