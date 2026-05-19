from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Comment


async def get_comments(db: AsyncSession):
    result = await db.execute(select(Comment))
    return result.scalars().all()


async def get_comment(db: AsyncSession, comment_id: int):
    result = await db.execute(select(Comment).where(Comment.id == comment_id))
    return result.scalar_one_or_none()


async def create_comment(db: AsyncSession, content: str, user_id: int, post_id: int):
    db_comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def delete_comment(db: AsyncSession, comment_id: int):
    db_comment = await get_comment(db, comment_id)
    if not db_comment:
        return None
    await db.delete(db_comment)
    await db.commit()
    return db_comment