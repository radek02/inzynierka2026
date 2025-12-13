"""Redis cache client"""

from typing import Optional, cast

import redis


class CacheClient:
    def __init__(self, host: str, port: int, db: int) -> None:
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
            socket_connect_timeout=5,
        )

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        try:
            if ttl:
                self.client.setex(key, ttl, value)
            else:
                self.client.set(key, value)
            return True
        except Exception:
            return False

    def get(self, key: str) -> Optional[str]:
        try:
            return cast(Optional[str], self.client.get(key))
        except Exception:
            return None

    def delete(self, key: str) -> bool:
        try:
            return cast(int, self.client.delete(key)) > 0
        except Exception:
            return False

    def ping(self) -> bool:
        try:
            return cast(bool, self.client.ping())
        except Exception:
            return False

    def close(self) -> None:
        self.client.close()
