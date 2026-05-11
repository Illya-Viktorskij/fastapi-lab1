from fastapi import APIRouter, HTTPException
from schemas.user import UserCreate, UserUpdate, UserResponse
from db.fake_db import fake_users_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


def get_next_id() -> int:
    return max(fake_users_db.keys(), default=0) + 1


# GET всіх юзерів
@router.get("/", response_model=List[UserResponse])
def get_users():
    return list(fake_users_db.values())


# GET одного юзера
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# POST створити юзера
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    new_id = get_next_id()
    new_user = {"id": new_id, **user.model_dump()}
    fake_users_db[new_id] = new_user
    return new_user


# PUT оновити юзера
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    updated = user_data.model_dump(exclude_unset=True)
    user.update(updated)
    return user


# DELETE видалити юзера
@router.delete("/{user_id}")
def delete_user(user_id: int):
    user = fake_users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    del fake_users_db[user_id]
    return {"message": f"User {user_id} deleted successfully"}