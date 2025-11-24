from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import UserRecmmendationResponse
from app.db import IEmbeddingsStorage
from app.core.dependency_container import get_embeddings_storage

recommendation_router = APIRouter()

@recommendation_router.get("/user-recommendations/{user_id}", response_model=UserRecmmendationResponse)
async def get_user_recommendations(user_id: int, service: IEmbeddingsStorage = Depends(get_embeddings_storage)):
    try:
        user_embeddings = service.get_user_embeddings(user_id)
        res = service.get_best_books(user_embeddings=user_embeddings, amount=2)

        return UserRecmmendationResponse(user_id=1, recommended_books=[(res[0]).book_id, (res[1]).book_id])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))