from redis.asyncio import Redis

from settings import settings


__all__ = ["async_redis_client"]

async_redis_client = Redis.from_url(url=settings.REDIS.POSTGRES_DSN.unicode_string())
