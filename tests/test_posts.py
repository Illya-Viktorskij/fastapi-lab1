from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.post import create_post, get_post, get_posts, delete_post
from app.crud.user import create_user
from app.schemas.user import UserCreate


async def test_crud_create_post(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="PostAuthor",
        email="postauthor@test.com",
        age=25
    ))
    post = await create_post(db, "Test Post", "Content", user.id)
    assert post.id is not None
    assert post.title == "Test Post"


async def test_crud_get_post(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="PostAuthor2",
        email="postauthor2@test.com",
        age=25
    ))
    post = await create_post(db, "Get Post", "Content", user.id)
    fetched = await get_post(db, post.id)
    assert fetched is not None


async def test_crud_get_posts(db: AsyncSession):
    posts = await get_posts(db)
    assert isinstance(posts, list)


async def test_crud_delete_post(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="PostAuthor3",
        email="postauthor3@test.com",
        age=25
    ))
    post = await create_post(db, "Del Post", "Content", user.id)
    deleted = await delete_post(db, post.id)
    assert deleted is not None


async def test_api_get_posts(client: AsyncClient):
    response = await client.get("/posts/")
    assert response.status_code == 200


async def test_api_create_post_authenticated(auth_client: AsyncClient):
    response = await auth_client.post("/posts/", json={
        "title": "Auth Post",
        "content": "Content here",
        "user_id": 1,
        "category_id": None
    })
    assert response.status_code == 201
    assert response.json()["title"] == "Auth Post"


async def test_api_create_post_unauthenticated(client: AsyncClient):
    response = await client.post("/posts/", json={
        "title": "No Auth Post",
        "content": "Content",
        "category_id": None
    })
    assert response.status_code == 401


async def test_api_my_posts(auth_client: AsyncClient):
    response = await auth_client.get("/posts/my")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_api_delete_post_not_owner(auth_client: AsyncClient, db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="OtherUser",
        email="otheruser@test.com",
        age=25
    ))
    post = await create_post(db, "Other Post", "Content", user.id)
    response = await auth_client.delete(f"/posts/{post.id}")
    assert response.status_code == 403