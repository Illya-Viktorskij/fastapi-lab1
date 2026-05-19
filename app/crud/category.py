from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import Category


async def get_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_category(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar_one_or_none()


async def create_category(db: AsyncSession, name: str, description: str = None):
    db_category = Category(name=name, description=description)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(db: AsyncSession, category_id: int):
    db_category = await get_category(db, category_id)
    if not db_category:
        return None
    await db.delete(db_category)
    await db.commit()
    return db_category