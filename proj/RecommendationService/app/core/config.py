from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    # Default values will be overriden if .env is present
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8080
    qdrant_url: str = "http://localhost:6333"

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "interactions"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = AppConfig()
