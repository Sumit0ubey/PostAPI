from pydantic import BaseModel, EmailStr, Field, field_serializer # type: ignore
from typing import Optional, Annotated
from datetime import datetime
from enum import Enum

from .utils import serialize_timestamp

class UserModel(BaseModel):
    name: str
    email: EmailStr
    phoneNo: Annotated[int, Field(gt=0)]

class createUser(UserModel):
    password: str
    confirm_password: str

class getUser(UserModel):
    id: int
    created_at: datetime

    @field_serializer("created_at")
    def timestamp_serializer(self, dt: datetime) -> str:
        return serialize_timestamp(dt)

    class Config:
        from_attributes  = True

class PostModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = Field(default=True)

class getPost(PostModel):
    id: int
    created_at: datetime

    @field_serializer("created_at")
    def timestamp_serializer(self, dt: datetime) -> str:
        return serialize_timestamp(dt)

    class Config:
        from_attributes  = True

class getPostWithLikes(getPost):
    user: str
    likes: int

class createPost(PostModel):
    pass

class updatePost(BaseModel):
    title: str
    content: str

    class Config:
        from_attributes = True

class LikeOrderEnum(int, Enum):
    LIKE = 0
    DISLIKE = 1

class likemodel(BaseModel):
    post_id: int
    order: LikeOrderEnum

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

