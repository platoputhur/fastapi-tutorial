from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from helpers.auth_utils import verify_password
from helpers.oauth2_utils import create_access_token, oauth2_scheme, verify_access_token
from managers.sqlalchemy_manager import get_db
from models.bal.schemas import UserAuthenticationRequest
from models.dal.models import User


class AuthManagerFactory:
    def __call__(self, use_orm=True, *args, **kwargs):
        if use_orm:
            return AuthManagerWithORM()


class AuthManager(ABC):
    @abstractmethod
    def authenticate(self, user: UserAuthenticationRequest, db): pass


class AuthManagerWithORM(AuthManager):

    def authenticate(self, user_credentials: UserAuthenticationRequest, db):
        user_from_db = db.query(User).filter_by(email=user_credentials.username).first()
        if not user_from_db:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.")
        if verify_password(user_credentials.password, user_from_db.password):
            access_token = create_access_token(data={"user_id": user_from_db.id})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.",
                                headers={"WWW_Authenticate": "Bearer"})


def verify_token_and_get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials.",
                                          headers={"WWW_Authenticate": "Bearer"})
    user_id = verify_access_token(token, credentials_exception)

    user = db.query(User).filter_by(id=user_id).first()
    return user
