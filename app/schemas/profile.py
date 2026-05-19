from pydantic import BaseModel
from typing import Optional


class ProfileCreate(BaseModel):
    user_id: int
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = {"from_attributes": True}