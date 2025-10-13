# pip install pydantic-settings

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:admin@localhost:5432/demo1"  # Provide a default or load from .env
    jwt_secret: str = "c866b7b3"        # Provide a default or load from .env
    jwt_alg: str = "HS256"
    access_token_expire_minutes: int = 30
    redis_url: str = "redis://localhost:6379/0"

    # v2-style configuration
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
