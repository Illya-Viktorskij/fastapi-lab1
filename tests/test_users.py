import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import create_user, get_user, get_users, update_user, delete_user
from app.schemas.user import UserCreate, UserUpdate


# CRUD тести
async def test_crud_create_user(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="CRUDUser",
        email="cruduser@test.com",
        age=30
    ))
    assert user.id is not None
    assert user.name == "CRUDUser"


async def test_crud_get_user(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="GetUser",
        email="getuser@test.com",
        age=25
    ))
    fetched = await get_user(db, user.id)
    assert fetched is not None
    assert fetched.email == "getuser@test.com"


async def test_crud_get_users(db: AsyncSession):
    users = await get_users(db)
    assert isinstance(users, list)


async def test_crud_update_user(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="UpdateUser",
        email="updateuser@test.com",
        age=20
    ))
    updated = await update_user(db, user.id, UserUpdate(name="UpdatedName"))
    assert updated.name == "UpdatedName"


async def test_crud_delete_user(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="DeleteUser",
        email="deleteuser@test.com",
        age=22
    ))
    deleted = await delete_user(db, user.id)
    assert deleted is not None
    assert await get_user(db, user.id) is None


# API тести
async def test_api_get_users(client: AsyncClient):
    response = await client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_api_create_user(client: AsyncClient):
    response = await client.post("/users/", json={
        "name": "APIUser",
        "email": "apiuser@test.com",
        "age": 25
    })
    assert response.status_code == 201
    assert response.json()["name"] == "APIUser"


async def test_api_get_user(client: AsyncClient):
    create = await client.post("/users/", json={
        "name": "SingleUser",
        "email": "singleuser@test.com",
        "age": 30
    })
    user_id = create.json()["id"]
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200


async def test_api_get_user_not_found(client: AsyncClient):
    response = await client.get("/users/99999")
    assert response.status_code == 404


async def test_api_update_user(client: AsyncClient):
    create = await client.post("/users/", json={
        "name": "OldName",
        "email": "oldname@test.com",
        "age": 25
    })
    user_id = create.json()["id"]
    response = await client.put(f"/users/{user_id}", json={"name": "NewName"})
    assert response.status_code == 200
    assert response.json()["name"] == "NewName"


async def test_api_delete_user(client: AsyncClient):
    create = await client.post("/users/", json={
        "name": "ToDelete",
        "email": "todelete@test.com",
        "age": 25
    })
    user_id = create.json()["id"]
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 200