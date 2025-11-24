from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import UserRecmmendationResponse

recommendation_router = APIRouter()

@recommendation_router.get("/user-recommendations/{user_id}", response_model=UserRecmmendationResponse)
async def get_user_recommendations(user_id: int, ):
    try:
        return UserRecmmendationResponse(user_id=1, recommended_books=[1, 2, 3])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))