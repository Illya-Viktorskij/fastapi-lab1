from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str
    user_id: int
    post_id: int


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    model_config = {"from_attributes": True}