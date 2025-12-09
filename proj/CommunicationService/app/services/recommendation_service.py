from app.db import CacheRecommendationRepository
from app.models import Book
from app.services.recommendation_client import RecommendationServiceClient


class RecommendationService:
    def __init__(
        self,
        cache: CacheRecommendationRepository,
        client: RecommendationServiceClient,
    ):
        self.cache = cache
        self.client = client

    def get_recommendations(self, user_id: int) -> tuple[list[Book], str]:
        cached = self.cache.try_get_user_recommendation(user_id)
        if cached:
            return (cached, "cache")

        book_ids = self.client.get_user_recommendations(user_id)
        books = [Book(book_id=bid) for bid in book_ids]
        self.cache.set_user_recommendation(user_id, books)
        return (books, "computed")
