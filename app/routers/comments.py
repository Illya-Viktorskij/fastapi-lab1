from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import comment as crud
from app.schemas.comment import CommentCreate, CommentResponse
from typing import List

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/", response_model=List[CommentResponse])
async def get_comments(db: AsyncSession = Depends(get_db)):
    return await crud.get_comments(db)


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(data: CommentCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_comment(db, data.content, data.user_id, data.post_id)


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await crud.delete_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": f"Comment {comment_id} deleted"}