import json

from app.models import Book
from app.services import CacheClient


class CacheRecommendationRepository:
    def __init__(self, cache: CacheClient, ttl: int = 3600):
        self.cache = cache
        self.ttl = ttl

    def _get_key(self, user_id: int) -> str:
        return f"recommendations:user:{user_id}"

    def try_get_user_recommendation(self, user_id: int) -> list[Book] | None:
        try:
            cached = self.cache.get(self._get_key(user_id))
            if not cached:
                return None
            data = json.loads(cached)
            return [Book(**item) for item in data]
        except Exception:
            return None

    def set_user_recommendation(
        self, user_id: int, recommendations: list[Book]
    ) -> None:
        data = [book.model_dump() for book in recommendations]
        self.cache.set(self._get_key(user_id), json.dumps(data), ttl=self.ttl)

    def delete_user_recommendation(self, user_id: int) -> None:
        self.cache.delete(self._get_key(user_id))
