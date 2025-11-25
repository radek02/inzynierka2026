from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    # Default values will be overriden if .env is present
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8080
    qdrant_url: str = "http://localhost:6333"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = AppConfig()
