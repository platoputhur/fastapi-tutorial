from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, validator


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


class PostWithVotesResponse(BaseModel):
    Post: PostResponse
    votes: int


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


class Vote(BaseModel):
    post_id: int


class VoteRequest(Vote):
    dir: int

    @validator('dir')
    def validate_vote(cls, val):
        if val != 0 and val != 1:
            raise ValueError('Invalid vote')
        else:
            return val
