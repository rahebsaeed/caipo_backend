# File: app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CAIPO Backend API"
    API_V1_STR: str = "/api/v1"
    # Later, you can add DB_URL, etc.

    class Config:
        env_file = ".env"

settings = Settings()