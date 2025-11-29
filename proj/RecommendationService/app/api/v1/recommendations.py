from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import UserRecmmendationResponse
from app.core.dependency_container import get_user_recommendation_orchestrator, get_interactions_repository
from app.services import UserRecommendationOrchestrator

recommendation_router = APIRouter()

@recommendation_router.get("/user-recommendations/{user_id}", response_model=UserRecmmendationResponse)
async def get_user_recommendations(user_id: int, service: UserRecommendationOrchestrator = Depends(get_user_recommendation_orchestrator)):
    try:
        result = service.get_user_recommendation(user_id=user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
