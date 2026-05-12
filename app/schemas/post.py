from pydantic import BaseModel
from typing import Optional


class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int
    category_id: Optional[int] = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    user_id: int
    category_id: Optional[int] = None

    model_config = {"from_attributes": True}