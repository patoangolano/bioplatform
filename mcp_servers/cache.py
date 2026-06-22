"""Redis caching layer for MCP adapters.

Provides an async decorator that caches function results in Redis
with configurable TTL per data source. Gracefully degrades to
pass-through if Redis is unavailable.

Cache key format: bio:cache:{prefix}:{func_name}:{sha256(args)[:16]}
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
from functools import wraps
from typing import Any, Callable, Type

logger = logging.getLogger(__name__)

_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
_pool = None


async def get_redis():
    """Get or create async Redis connection pool."""
    global _pool
    if _pool is None:
        try:
            import redis.asyncio as aioredis
            _pool = aioredis.from_url(_REDIS_URL, decode_responses=True)
            await _pool.ping()
            logger.info("Redis cache connected: %s", _REDIS_URL)
        except Exception as e:
            logger.warning("Redis cache unavailable, operating without cache: %s", e)
            _pool = None
    return _pool


def _make_key(prefix: str, func_name: str, args: tuple, kwargs: dict) -> str:
    """Generate deterministic cache key from function arguments."""
    raw = json.dumps(
        {"a": [str(a) for a in args], "kw": {k: str(v) for k, v in sorted(kwargs.items())}},
        sort_keys=True,
    )
    h = hashlib.sha256(raw.encode()).hexdigest()[:16]
    return f"bio:cache:{prefix}:{func_name}:{h}"


def _serialize(result: Any) -> str:
    """Serialize result to JSON string."""
    if hasattr(result, "model_dump"):
        return json.dumps(result.model_dump())
    if isinstance(result, list) and result and hasattr(result[0], "model_dump"):
        return json.dumps([item.model_dump() for item in result])
    return json.dumps(result)


def cached(ttl: int, prefix: str, model: Type | None = None, is_list: bool = False):
    """Async cache decorator for MCP adapter functions.

    Args:
        ttl: Time-to-live in seconds.
        prefix: Cache namespace prefix (e.g., "uniprot", "pubmed").
        model: Pydantic model class for deserialization on cache hit.
        is_list: If True, result is a list of model instances.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            r = await get_redis()
            if r is None:
                return await func(*args, **kwargs)

            key = _make_key(prefix, func.__name__, args, kwargs)

            try:
                hit = await r.get(key)
                if hit is not None:
                    data = json.loads(hit)
                    if model is not None:
                        if is_list:
                            return [model.model_validate(item) for item in data]
                        return model.model_validate(data)
                    return data
            except Exception as e:
                logger.debug("Cache read error (key=%s): %s", key, e)

            result = await func(*args, **kwargs)

            try:
                serialized = _serialize(result)
                await r.setex(key, ttl, serialized)
            except Exception as e:
                logger.debug("Cache write error (key=%s): %s", key, e)

            return result
        return wrapper
    return decorator
