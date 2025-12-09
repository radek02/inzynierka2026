from collections.abc import Generator

import psycopg2
import psycopg2.extensions
from fastapi import Depends

from app.core.config import AppConfig, settings
from app.services import CacheClient, RecommendationServiceClient


def get_settings() -> AppConfig:
    return settings


def get_db(
    config: AppConfig = Depends(get_settings),
) -> Generator[psycopg2.extensions.connection, None, None]:
    """Dependency for database connection"""
    conn = psycopg2.connect(
        host=config.postgres_host,
        port=config.postgres_port,
        database=config.postgres_db,
        user=config.postgres_user,
        password=config.postgres_password,
    )
    try:
        yield conn
    finally:
        conn.close()


def get_cache(
    config: AppConfig = Depends(get_settings),
) -> Generator[CacheClient, None, None]:
    """Dependency for cache"""
    client = CacheClient(config.redis_host, config.redis_port, config.redis_db)
    try:
        yield client
    finally:
        client.close()


def get_recommendation_client(
    config: AppConfig = Depends(get_settings),
) -> RecommendationServiceClient:
    """Dependency for recommendation service client"""
    return RecommendationServiceClient(base_url=config.recommendation_service_url)
