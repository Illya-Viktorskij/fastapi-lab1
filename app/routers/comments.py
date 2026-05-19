from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud import comment as crud
from app.schemas.comment import CommentCreate, CommentResponse
from app.metrics import TOTAL_COMMENTS, CRUD_OPERATIONS_TOTAL
from typing import List

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/", response_model=List[CommentResponse])
async def get_comments(db: AsyncSession = Depends(get_db)):
    comments = await crud.get_comments(db)
    TOTAL_COMMENTS.set(len(comments))
    CRUD_OPERATIONS_TOTAL.labels(operation="read", entity="comment").inc()
    return comments


@router.get("/{comment_id}", response_model=CommentResponse)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await crud.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    CRUD_OPERATIONS_TOTAL.labels(operation="read", entity="comment").inc()
    return comment


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(data: CommentCreate, db: AsyncSession = Depends(get_db)):
    comment = await crud.create_comment(db, data.content, data.user_id, data.post_id)
    CRUD_OPERATIONS_TOTAL.labels(operation="create", entity="comment").inc()
    return comment


@router.delete("/{comment_id}")
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    comment = await crud.delete_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    CRUD_OPERATIONS_TOTAL.labels(operation="delete", entity="comment").inc()
    return {"message": f"Comment {comment_id} deleted"}