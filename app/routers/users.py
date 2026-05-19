from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import user as crud
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.metrics import TOTAL_USERS, CRUD_OPERATIONS_TOTAL
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await crud.get_users(db)
    TOTAL_USERS.set(len(users))
    CRUD_OPERATIONS_TOTAL.labels(operation="read", entity="user").inc()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    CRUD_OPERATIONS_TOTAL.labels(operation="read", entity="user").inc()
    return user


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.create_user(db, user)
    users = await crud.get_users(db)
    TOTAL_USERS.set(len(users))
    CRUD_OPERATIONS_TOTAL.labels(operation="create", entity="user").inc()
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await crud.update_user(db, user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    CRUD_OPERATIONS_TOTAL.labels(operation="update", entity="user").inc()
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    users = await crud.get_users(db)
    TOTAL_USERS.set(len(users))
    CRUD_OPERATIONS_TOTAL.labels(operation="delete", entity="user").inc()
    return {"message": f"User {user_id} deleted successfully"}