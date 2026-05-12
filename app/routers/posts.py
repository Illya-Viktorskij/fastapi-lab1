from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import post as crud
from app.schemas.post import PostCreate, PostResponse
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    return await crud.get_posts(db)


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(data: PostCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_post(db, data.title, data.content, data.user_id, data.category_id)


@router.delete("/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await crud.delete_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": f"Post {post_id} deleted"}