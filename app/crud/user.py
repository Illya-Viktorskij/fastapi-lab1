from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User
from app.schemas.user import UserCreate, UserUpdate


async def get_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate):
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
    for key, value in user_data.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    db_user = await get_user(db, user_id)
    if not db_user:
        return None
    await db.delete(db_user)
    await db.commit()
    return db_user