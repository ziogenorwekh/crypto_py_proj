from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    DATABASE_URL: str
    UPBIT_ACCESS_KEY: str | None = None
    UPBIT_SECRET_KEY: str | None = None

    PROJECT_NAME: str = "crypto Real-time Analysis"

    TELEGRAM_TOKEN: str | None = None
    TELEGRAM_CHAT_ID: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding='utf-8'
    )


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
