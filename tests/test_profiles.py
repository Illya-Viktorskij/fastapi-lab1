from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.profile import create_profile, get_profile, delete_profile
from app.crud.user import create_user
from app.schemas.user import UserCreate


async def test_crud_create_profile(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="ProfileUser",
        email="profileuser@test.com",
        age=25
    ))
    profile = await create_profile(db, user.id, "Bio here", "http://avatar.com")
    assert profile.id is not None
    assert profile.bio == "Bio here"


async def test_crud_get_profile(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="ProfileUser2",
        email="profileuser2@test.com",
        age=25
    ))
    await create_profile(db, user.id, "Bio", None)
    fetched = await get_profile(db, user.id)
    assert fetched is not None


async def test_crud_delete_profile(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="ProfileUser3",
        email="profileuser3@test.com",
        age=25
    ))
    await create_profile(db, user.id, "Bio", None)
    deleted = await delete_profile(db, user.id)
    assert deleted is not None


async def test_api_create_profile(client: AsyncClient, db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="APIProfileUser",
        email="apiprofileuser@test.com",
        age=25
    ))
    response = await client.post("/profiles/", json={
        "user_id": user.id,
        "bio": "Test bio",
        "avatar_url": None
    })
    assert response.status_code == 201


async def test_api_get_profile_not_found(client: AsyncClient):
    response = await client.get("/profiles/99999")
    assert response.status_code == 404