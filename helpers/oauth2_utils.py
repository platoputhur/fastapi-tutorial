from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from helpers.config import settings
from models.bal.schemas import TokenData

SECRET_KEY = settings.auth_secret  # "2f9d4b9326d6c29c18377877281c9d5cc58aff29a431d851cb9a0f211d60f779"
ALGORITHM = settings.auth_algorithm  # "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.auth_expiry_in_minutes  # 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expiry})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = decoded_token.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data.id
