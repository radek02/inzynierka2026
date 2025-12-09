import psycopg2.extensions
from fastapi import Depends

from app.core import get_cache, get_db, get_recommendation_client, get_settings
from app.core.config import AppConfig
from app.db import CacheRecommendationRepository, InteractionsRepository
from app.services import CacheClient, RecommendationService, RecommendationServiceClient


def get_interactions_repo(
    db: psycopg2.extensions.connection = Depends(get_db),
) -> InteractionsRepository:
    return InteractionsRepository(db)


def get_cache_repo(
    cache: CacheClient = Depends(get_cache),
    config: AppConfig = Depends(get_settings),
) -> CacheRecommendationRepository:
    return CacheRecommendationRepository(cache, ttl=config.cache_ttl)


def get_recommendation_service(
    cache_repo: CacheRecommendationRepository = Depends(get_cache_repo),
    client: RecommendationServiceClient = Depends(get_recommendation_client),
) -> RecommendationService:
    return RecommendationService(cache_repo, client)
