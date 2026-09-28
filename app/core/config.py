"""
Application Configuration
All settings are loaded from environment variables with sensible defaults.
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Student Management API"
    PROJECT_DESCRIPTION: str = (
        "A RESTful API for managing student records — "
        "built with FastAPI and deployed via CI/CD on Render."
    )
    VERSION: str = "1.0.0"

    # API
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"

    # Database
    DATABASE_URL: str = "sqlite:///./students.db"

    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]

    # Environment
    ENVIRONMENT: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
