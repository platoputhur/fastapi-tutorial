from pydantic import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_db_url: str = ""
    auth_secret: str = ""
    auth_algorithm: str = ""
    auth_expiry_in_minutes: int = 0

    class Config:
        env_file = ".env"


settings = Settings()
