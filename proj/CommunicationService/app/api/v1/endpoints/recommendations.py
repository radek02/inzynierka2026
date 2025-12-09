from app.api.dependencies import get_cache_repo, get_recommendation_client
from app.db import CacheRecommendationRepository
from app.models import Book, RecommendationsResponse
from app.services import RecommendationService
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(
    user_id: int,
    cache_repo: CacheRecommendationRepository = Depends(get_cache_repo),
    service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendationsResponse:
    try:
        recommendations, source = service.get_recommendations(user_id)
        return RecommendationsResponse(
            user_id=user_id, recommendations=recommendations, source=source
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get recommendations: {str(e)}"
        )
