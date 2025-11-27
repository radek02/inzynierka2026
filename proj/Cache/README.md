# Cache Service

Redis instance for caching recommendations.

## Quick Start

```bash
docker build -t redis-cache .
docker run -d --name redis -p 6379:6379 redis-cache
```

## Environment Variables

Services connecting to Redis use:

- `REDIS_HOST` - Redis host (default: localhost)
- `REDIS_PORT` - Redis port (default: 6379)
- `REDIS_DB` - Redis database number (default: 0)
