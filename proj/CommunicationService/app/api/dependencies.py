from fastapi import Depends

from app.core import get_cache, get_db, settings
from app.db import CacheRecommendationRepository, InteractionsRepository


def get_interactions_repo(db=Depends(get_db)) -> InteractionsRepository:
    return InteractionsRepository(db)


def get_cache_repo(cache=Depends(get_cache)) -> CacheRecommendationRepository:
    return CacheRecommendationRepository(cache, ttl=settings.cache_ttl)
