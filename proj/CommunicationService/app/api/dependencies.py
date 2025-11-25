import psycopg2
import psycopg2.extensions
from Cache.cache_client import CacheClient
from fastapi import Depends

from app.core import get_cache, get_db, settings
from app.db import CacheRecommendationRepository, InteractionsRepository
from app.services import RecommendationServiceClient


def get_interactions_repo(
    db: psycopg2.extensions.connection = Depends(get_db),
) -> InteractionsRepository:
    return InteractionsRepository(db)


def get_cache_repo(
    cache: CacheClient = Depends(get_cache),
) -> CacheRecommendationRepository:
    return CacheRecommendationRepository(cache, ttl=settings.cache_ttl)


def get_recommendation_client() -> RecommendationServiceClient:
    return RecommendationServiceClient(base_url=settings.recommendation_service_url)
