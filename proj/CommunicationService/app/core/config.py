from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "interactions"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    recommendation_service_url: str = "http://localhost:8001"
    cache_ttl: int = 24 * 3600  # 24 hours

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = AppConfig()
