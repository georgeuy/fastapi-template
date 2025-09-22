from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # project settings
    PROJECT_NAME: str = "FastAPI Template"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")

    class Config:
        env_file = ".env"


settings = Settings()
