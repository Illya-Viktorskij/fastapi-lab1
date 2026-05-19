from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Post


async def get_posts(db: AsyncSession):
    result = await db.execute(select(Post))
    return result.scalars().all()


async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()


async def create_post(db: AsyncSession, title: str, content: str, user_id: int, category_id: int = None):
    db_post = Post(title=title, content=content, user_id=user_id, category_id=category_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


async def delete_post(db: AsyncSession, post_id: int):
    db_post = await get_post(db, post_id)
    if not db_post:
        return None
    await db.delete(db_post)
    await db.commit()
    return db_post

async def get_posts_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(Post).where(Post.user_id == user_id))
    return result.scalars().all()