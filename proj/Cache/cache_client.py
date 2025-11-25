"""
Simple Redis client for CommunicationService
"""

import os
from typing import Optional, cast
    
import redis
from dotenv import load_dotenv

load_dotenv()


class CacheClient:
    def __init__(self) -> None:
        self.client = redis.Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            decode_responses=True,
            socket_connect_timeout=5,
        )

    def set(self, key: str, value: str, ttl: Optional[int] = None) -> bool:
        """Set a cache value"""
        try:
            if ttl:
                self.client.setex(key, ttl, value)
            else:
                self.client.set(key, value)
            return True
        except Exception:
            return False

    def get(self, key: str) -> Optional[str]:
        """Get a cache value"""
        try:
            return cast(Optional[str], self.client.get(key))
        except Exception:
            return None

    def delete(self, key: str) -> bool:
        """Delete a cache value"""
        try:
            return cast(bool, self.client.delete(key) > 0)
        except Exception:
            return False

    def ping(self) -> bool:
        """Check if Redis is reachable"""
        try:
            return cast(bool, self.client.ping())
        except Exception:
            return False

    def close(self) -> None:
        """Close Redis connection"""
        self.client.close()
