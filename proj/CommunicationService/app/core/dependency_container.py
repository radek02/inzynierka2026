from collections.abc import Generator

import psycopg2
import psycopg2.extensions

from app.core.config import AppConfig, settings
from app.services import CacheClient


def get_settings() -> AppConfig:
    return settings


def get_db() -> Generator[psycopg2.extensions.connection, None, None]:
    """Dependency for database connection"""
    conn = psycopg2.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        database=settings.postgres_db,
        user=settings.postgres_user,
        password=settings.postgres_password,
    )
    try:
        yield conn
    finally:
        conn.close()


def get_cache() -> Generator[CacheClient, None, None]:
    """Dependency for cache"""
    client = CacheClient()
    try:
        yield client
    finally:
        client.close()
