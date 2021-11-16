from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from managers.auth_manager import AuthManagerFactory
from models.bal.schemas import UserAuthenticationResponse

router = APIRouter(tags=['Authentication'])

auth_factory = AuthManagerFactory()
auth_manager = auth_factory()


@router.post("/login", response_model=UserAuthenticationResponse)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    # We are using OAuth2PasswordRequestForm to follow the oauth2 spec which says we have to use
    # username and password keys in the dict sent for user auth. It can't be anything else.
    token = auth_manager.authenticate(user_credentials)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    else:
        return token
