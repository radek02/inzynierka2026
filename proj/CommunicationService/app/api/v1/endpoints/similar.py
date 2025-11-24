from app.models import SimilarResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/similar", response_model=SimilarResponse)
async def get_similar_books(book_id: int):
    """Get similar books - follows lab2 spec"""
    # TODO: Implement when Recommender Module is ready
    return SimilarResponse(book_id=book_id, similar_books=[])
