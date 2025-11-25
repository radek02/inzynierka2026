from app.api.dependencies import get_cache_repo
from app.db import CacheRecommendationRepository
from app.models import Book, RecommendationsResponse
from app.services import RecommendationServiceClient
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(
    user_id: int,
    cache_repo: CacheRecommendationRepository = Depends(get_cache_repo),
) -> RecommendationsResponse:
    # Check cache first
    cached = cache_repo.try_get_user_recommendation(user_id)
    if cached:
        return RecommendationsResponse(
            user_id=user_id, recommendations=cached, source="cache"
        )

    # Call RecommendationService
    try:
        client = RecommendationServiceClient()
        book_ids = client.get_user_recommendations(user_id)

        # Convert book IDs to Book objects
        recommendations = [Book(book_id=book_id) for book_id in book_ids]

        # Cache the results
        cache_repo.set_user_recommendation(user_id, recommendations)

        return RecommendationsResponse(
            user_id=user_id, recommendations=recommendations, source="computed"
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get recommendations: {str(e)}"
        )
