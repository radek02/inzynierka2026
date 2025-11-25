from app.api.dependencies import get_cache_repo, get_interactions_repo
from app.db import CacheRecommendationRepository, InteractionsRepository
from app.models import InteractionsRequest, InteractionsResponse
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.post(
    "/interactions",
    response_model=InteractionsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user-book interaction",
    description="Add or update a user's rating for a book. Invalidates cached recommendations.",
)
async def register_interaction(
    request: InteractionsRequest,
    interaction_repo: InteractionsRepository = Depends(get_interactions_repo),
    cache_repo: CacheRecommendationRepository = Depends(get_cache_repo),
) -> InteractionsResponse:
    try:
        success = interaction_repo.insert_new_interaction(
            request.user_id, request.book_id, request.rating
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to insert")

        # Invalidate cache
        cache_repo.delete_user_recommendation(request.user_id)

        return InteractionsResponse(
            message="Interaction registered successfully",
            user_id=request.user_id,
            book_id=request.book_id,
            rating=request.rating,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
