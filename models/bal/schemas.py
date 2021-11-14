from datetime import datetime

from pydantic import BaseModel, EmailStr


# Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    class Config:
        orm_mode = True


class PostCreateRequest(PostBase):
    pass


class PostUpdateRequest(PostBase):
    pass


class PostResponse(PostBase):
    id: str
    created_at: datetime


# Users
class UserBase(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreateRequest(UserBase):
    password: str


class UserResponse(UserBase):
    id: str
    email: str
    created_at: datetime
