from typing import List, Any
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
import json
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # project settings
    PROJECT_NAME: str = "FastAPI Template"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")

    # Server settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    # API settings
    DOCS_URL: str = "/docs"
    REDOC_URL: str = "/redoc"

    # cors - USAMOS Any PARA EVITAR CONFLICTOS DE TYPING
    ALLOW_ORIGINS: Any = Field(
        default=["http://localhost:3000"],
        description="List of allowed CORS origins",
        env="ALLOW_ORIGINS",
    )

    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./app.db", env="DATABASE_URL"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @field_validator("ALLOW_ORIGINS", mode="before")
    @classmethod
    def parse_allow_origins(cls, value: Any) -> List[str]:
        """Parse ALLOW_ORIGINS from various formats to list"""
        if isinstance(value, list):
            return value

        if isinstance(value, str):
            value = value.strip()
            if not value:
                return []

            # Intenta parsear como JSON primero
            if value.startswith("[") and value.endswith("]"):
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        return parsed
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON ALLOW_ORIGINS: {value}")
                    pass  # Continúa con otros formatos

            # Parsear como comma-separated
            if "," in value:
                return [origin.strip() for origin in value.split(",") if origin.strip()]

            # Parsear como space-separated
            return [origin.strip() for origin in value.split() if origin.strip()]

        # Si es cualquier otro tipo, devolver default
        logger.warning(f"Unsupported ALLOW_ORIGINS type: {type(value)}")
        return ["http://localhost:3000"]

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value: Any) -> bool:
        """Parse DEBUG from various formats to bool"""
        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            value = value.strip().lower()
            return value in ["true", "1", "yes", "on", "y"]

        if isinstance(value, int):
            return bool(value)

        return False


settings = Settings()
