from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import profile as crud
from app.schemas.profile import ProfileCreate, ProfileResponse
from app.metrics import CRUD_OPERATIONS_TOTAL

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    profile = await crud.get_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    CRUD_OPERATIONS_TOTAL.labels(operation="read", entity="profile").inc()
    return profile


@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(data: ProfileCreate, db: AsyncSession = Depends(get_db)):
    CRUD_OPERATIONS_TOTAL.labels(operation="create", entity="profile").inc()
    return await crud.create_profile(db, data.user_id, data.bio, data.avatar_url)


@router.delete("/{user_id}")
async def delete_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    profile = await crud.delete_profile(db, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    CRUD_OPERATIONS_TOTAL.labels(operation="delete", entity="profile").inc()
    return {"message": f"Profile for user {user_id} deleted"}