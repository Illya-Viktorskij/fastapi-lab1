from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.comment import create_comment, get_comment, get_comments, delete_comment
from app.crud.post import create_post
from app.crud.user import create_user
from app.schemas.user import UserCreate


async def test_crud_create_comment(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="CommentAuthor",
        email="commentauthor@test.com",
        age=25
    ))
    post = await create_post(db, "Post for comment", "Content", user.id)
    comment = await create_comment(db, "Nice post!", user.id, post.id)
    assert comment.id is not None
    assert comment.content == "Nice post!"


async def test_crud_get_comment(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="CommentAuthor2",
        email="commentauthor2@test.com",
        age=25
    ))
    post = await create_post(db, "Post2", "Content", user.id)
    comment = await create_comment(db, "Hello!", user.id, post.id)
    fetched = await get_comment(db, comment.id)
    assert fetched is not None


async def test_crud_get_comments(db: AsyncSession):
    comments = await get_comments(db)
    assert isinstance(comments, list)


async def test_crud_delete_comment(db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="CommentAuthor3",
        email="commentauthor3@test.com",
        age=25
    ))
    post = await create_post(db, "Post3", "Content", user.id)
    comment = await create_comment(db, "Delete me", user.id, post.id)
    deleted = await delete_comment(db, comment.id)
    assert deleted is not None


async def test_api_get_comments(client: AsyncClient):
    response = await client.get("/comments/")
    assert response.status_code == 200


async def test_api_create_comment(client: AsyncClient, db: AsyncSession):
    user = await create_user(db, UserCreate(
        name="APICommentUser",
        email="apicommentuser@test.com",
        age=25
    ))
    post = await create_post(db, "API Comment Post", "Content", user.id)
    response = await client.post("/comments/", json={
        "content": "API Comment",
        "user_id": user.id,
        "post_id": post.id
    })
    assert response.status_code == 201


async def test_api_comment_not_found(client: AsyncClient):
    response = await client.get("/comments/99999")
    assert response.status_code == 404