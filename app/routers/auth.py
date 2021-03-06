from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from managers.auth_manager import AuthManagerFactory
from managers.sqlalchemy_manager import get_db
from models.bal.schemas import UserAuthenticationResponse

router = APIRouter(tags=['Authentication'])

auth_factory = AuthManagerFactory()
auth_manager = auth_factory()


@router.post("/login", response_model=UserAuthenticationResponse)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # We are using OAuth2PasswordRequestForm to follow the oauth2 spec which says we have to use
    # username and password keys in the dict sent for user auth. It can't be anything else.
    token = auth_manager.authenticate(user_credentials, db)
    return token
