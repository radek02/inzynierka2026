# Cache Service

It is just a Redis instance and a simple Python client. 

## Quick Start

### 1. Run Redis

```bash
docker build -t redis-cache .
docker run -d --name redis -p 6379:6379 redis-cache
```

### 2. Use in CommunicationService

```python
from Cache.cache_client import CacheClient

cache = CacheClient()  # Uses localhost:6379 by default

# Set value (with optional TTL)
cache.set("user:123:recommendations", "[1,2,3]", ttl=3600)

# Get value
value = cache.get("user:123:recommendations")

# Delete value
cache.delete("user:123:recommendations")

# Check connection
if cache.ping():
    print("Redis is alive!")
```

## Environment Variables

Set in `.env` file:

- `REDIS_HOST` - Redis host (default: localhost)
- `REDIS_PORT` - Redis port (default: 6379)
- `REDIS_DB` - Redis database number (default: 0)

## Why no FastAPI?

Direct Redis connection is faster and simpler. No need for HTTP overhead when services can connect directly.
