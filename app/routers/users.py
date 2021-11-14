from typing import List

from fastapi import HTTPException, status, APIRouter

from managers.users_manager import UsersManagerFactory
from models.bal.schemas import UserResponse, UserCreateRequest

router = APIRouter()
users_factory = UsersManagerFactory()
users_manager = users_factory()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(new_user: UserCreateRequest):
    user = users_manager.create_user(new_user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return user


@router.get("/users", response_model=List[UserResponse])
def get_users():
    users = users_manager.get_users()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = users_manager.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} couldn't be found.")
    else:
        return user
