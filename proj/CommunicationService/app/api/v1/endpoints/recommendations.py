from app.api.dependencies import get_cache_repo
from app.db import CacheRecommendationRepository
from app.models import Book, RecommendationsResponse
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(
    user_id: int,
    cache_repo: CacheRecommendationRepository = Depends(get_cache_repo),
):
    cached = cache_repo.try_get_user_recommendation(user_id)

    if cached:
        return RecommendationsResponse(cached)

    # TODO: Call Recommender Module when implemented
    # For now return empty
    return RecommendationsResponse([])
