from pathlib import Path
from typing import Literal

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    # Logging settings
    LOG_LEVEL: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = "INFO"
    LOG_DIR: str | Path = BASE_DIR / "logs"
    LOG_FILE: str = "alice.log"
    LOG_FILE_SIZE: int = 10 * 2**20
    LOG_FILES_COUNT: int = 10

    # MongoDB settings
    ME_CONFIG_MONGODB_URL: str
    ME_CONFIG_MONGODB_ADMINUSERNAME: str
    ME_CONFIG_MONGODB_ADMINPASSWORD: str

    SENTRY_DSN: AnyHttpUrl
    BASE_AUDIO_URL: AnyHttpUrl = (
        "https://www.guidedogs.acceleratorpracticum.ru/"
    )

    QUIZ_FILE_PATH: str | Path = BASE_DIR / "app" / "quiz" / "quiz.json"


settings = Settings()
