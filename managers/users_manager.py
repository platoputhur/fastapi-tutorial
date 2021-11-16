from abc import abstractmethod, ABC

from sqlalchemy.orm import Session

from helpers.auth_utils import hash_password
from managers.sqlalchemy_manager import get_db
from models.bal.schemas import UserCreateRequest
from models.dal.models import User


class UsersManagerFactory:
    def __call__(self, use_orm=True, *args, **kwargs):
        if use_orm:
            return UsersManagerWithORM()
        # else:
        #     return UsersManagerWithoutORM()


class UsersManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_user(self, user: UserCreateRequest):
        pass

    @abstractmethod
    def get_user(self, user_id):
        pass

    @abstractmethod
    def get_users(self):
        pass

    @abstractmethod
    def update_user(self):
        pass

    @abstractmethod
    def delete_user(self):
        pass


class UsersManagerWithORM(UsersManager):

    def create_user(self, user: UserCreateRequest):
        db: Session = get_db()
        user.password = hash_password(user.password)
        new_user = User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_user(self, user_id):
        db: Session = get_db()
        user = db.query(User).filter_by(id=user_id).first()
        return user

    def get_users(self):
        db: Session = get_db()
        users = db.query(User).all()
        return users

    def update_user(self):
        pass

    def delete_user(self):
        pass
