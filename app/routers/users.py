from typing import List

from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

from managers.sqlalchemy_manager import get_db
from managers.users_manager import UsersManagerFactory
from models.bal.schemas import UserResponse, UserCreateRequest

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

users_factory = UsersManagerFactory()
users_manager = users_factory()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(new_user: UserCreateRequest, db: Session = Depends(get_db)):
    user = users_manager.create_user(new_user, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return user


@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = users_manager.get_users(db)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = users_manager.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} couldn't be found.")
    else:
        return user
