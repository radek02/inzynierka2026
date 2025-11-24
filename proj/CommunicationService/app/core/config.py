from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "interactions"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_ttl: int = 3600

    # FastAPI
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000

    # Recommender Service (for future)
    recommender_service_url: str = "http://localhost:8001"

    class Config:
        env_file = ".env"


settings = AppConfig()
