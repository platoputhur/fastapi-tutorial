from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


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
    owner_id: str
    owner: UserResponse


# Authentication
class AuthBase(BaseModel):
    class Config:
        orm_mode = True


class UserAuthenticationRequest(AuthBase):
    # This is username and not email is because oauth2 spec says the credentials must be sent with the keys
    # username and password and not anything else. The db can store it in whatever name, in our case it is email.
    # More information is given inside the auth route.
    username: EmailStr
    password: str


class UserAuthenticationResponse(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
