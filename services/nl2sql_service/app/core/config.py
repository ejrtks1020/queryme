import os
from pydantic_settings import BaseSettings

PROFILE = os.getenv("PROFILE", "local")

def get_env_path(profile: str) -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        f'env/.env.{profile}'
    )


class Config:
    extra = "allow"
    env_file = [
        get_env_path(PROFILE)
    ]
    env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    class Config(Config):
        pass

    GOOGLE_GEMINI_API_KEY: str
    CONNECTION_SERVICE_URL: str
    DDL_SESSION_SERVICE_URL: str
    HISTORY_SERVICE_URL: str


settings = Settings()