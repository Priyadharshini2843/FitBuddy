import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration and environment variables."""

    # Gemini API Credentials and Models
    google_api_key: str = ""
    gemini_pro_model: str = "gemini-1.5-pro"
    gemini_flash_model: str = "gemini-1.5-flash"

    # Database
    database_url: str = "sqlite:///./fitbuddy.db"

    # Runtime Settings
    app_env: str = "development"
    debug: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()