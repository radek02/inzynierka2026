import json

from redis import Redis

from app.models import Book


class CacheRecommendationRepository:
    def __init__(self, cache: Redis, ttl: int = 3600):
        self.cache = cache
        self.ttl = ttl

    def try_get_user_recommendation(self, user_id: int) -> list[Book] | None:
        try:
            key = f"recommendations:user:{user_id}"
            cached = self.cache.get(key)
            return json.loads(cached) if cached else None
        except Exception:
            return None

    def set_user_recommendation(
        self, user_id: int, recommendations: list[Book]
    ) -> None:
        key = f"recommendations:user:{user_id}"
        self.cache.setex(key, self.ttl, json.dumps(recommendations))

    def delete_user_recommendation(self, user_id: int) -> None:
        key = f"recommendations:user:{user_id}"
        self.cache.delete(key)
