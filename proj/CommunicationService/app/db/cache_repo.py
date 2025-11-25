import json

from Cache.cache_client import CacheClient
from app.models import Book


class CacheRecommendationRepository:
    def __init__(self, cache: CacheClient, ttl: int = 3600):
        self.cache = cache
        self.ttl = ttl

    def _get_key(self, user_id: int) -> str:
        return f"recommendations:user:{user_id}"

    def try_get_user_recommendation(self, user_id: int) -> list[Book] | None:
        try:
            cached = self.cache.get(self._get_key(user_id))
            return json.loads(cached) if cached else None
        except Exception:
            return None

    def set_user_recommendation(
        self, user_id: int, recommendations: list[Book]
    ) -> None:
        self.cache.set(self._get_key(user_id), json.dumps(recommendations), ttl=self.ttl)

    def delete_user_recommendation(self, user_id: int) -> None:
        self.cache.delete(self._get_key(user_id))
