from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Lead Management API"
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    # Fallback for Railway/Cloud providers
    MYSQL_URL: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    API_KEY: str = "omc_secret_key_123"
    RATE_LIMIT_PER_MINUTE: int = 60

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
