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

class DBConfig(BaseSettings):
    class Config(Config):
        pass    
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

db_config = DBConfig()
