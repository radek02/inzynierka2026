from app.db import CacheRecommendationRepository, InteractionsRepository
from app.models import Interaction


class InteractionError(Exception):
    """Failed to register interaction"""


class InteractionsService:
    def __init__(
        self,
        interactions_repo: InteractionsRepository,
        cache_repo: CacheRecommendationRepository,
    ):
        self.interactions_repo = interactions_repo
        self.cache_repo = cache_repo

    def register_interaction(self, user_id: int, book_id: int, rating: int) -> Interaction:
        interaction = self.interactions_repo.insert_new_interaction(
            user_id=user_id, book_id=book_id, rating=rating
        )

        if not interaction:
            raise InteractionError("Failed to insert interaction")

        self.cache_repo.delete_user_recommendation(user_id)
        return interaction
