from app.db import CacheRecommendationRepository, InteractionsRepository


class InteractionsService:
    def __init__(
        self,
        interactions_repo: InteractionsRepository,
        cache_repo: CacheRecommendationRepository,
    ):
        self.interactions_repo = interactions_repo
        self.cache_repo = cache_repo

    def register_interaction(self, user_id: int, book_id: int, rating: int) -> bool:
        success = self.interactions_repo.insert_new_interaction(
            user_id=user_id, book_id=book_id, rating=rating
        )

        if success:
            self.cache_repo.delete_user_recommendation(user_id)

        return success
