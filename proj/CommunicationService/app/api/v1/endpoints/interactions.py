from app.api.dependencies import get_interactions_service
from app.models import InteractionsRequest, InteractionsResponse
from app.services import InteractionsService
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
    service: InteractionsService = Depends(get_interactions_service),
) -> InteractionsResponse:
    try:
        interaction = service.register_interaction(
            user_id=request.user_id, book_id=request.book_id, rating=request.rating
        )
        return InteractionsResponse(
            message="Interaction registered successfully",
            interaction=interaction,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to register interaction: {str(e)}"
        )
