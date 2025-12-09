from app.api.dependencies import get_recommendation_service
from app.models import RecommendationsResponse
from app.services import RecommendationService
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get("/recommendations", response_model=RecommendationsResponse)
async def get_recommendations(
    user_id: int,
    service: RecommendationService = Depends(get_recommendation_service),
) -> RecommendationsResponse:
    try:
        recommendation = service.get_recommendations(user_id)
        return RecommendationsResponse(recommendation=recommendation)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get recommendations: {str(e)}"
        )
