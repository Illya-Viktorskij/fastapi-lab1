from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Profile


async def get_profile(db: AsyncSession, user_id: int):
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    return result.scalar_one_or_none()


async def create_profile(db: AsyncSession, user_id: int, bio: str = None, avatar_url: str = None):
    db_profile = Profile(user_id=user_id, bio=bio, avatar_url=avatar_url)
    db.add(db_profile)
    await db.commit()
    await db.refresh(db_profile)
    return db_profile


async def delete_profile(db: AsyncSession, user_id: int):
    db_profile = await get_profile(db, user_id)
    if not db_profile:
        return None
    await db.delete(db_profile)
    await db.commit()
    return db_profile