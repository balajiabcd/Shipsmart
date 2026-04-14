"""
Rate limiting and caching middleware.
"""

import time
import logging
from typing import Optional, Callable
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from .config import settings

logger = logging.getLogger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: dict = {}

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        minute_key = int(now / 60)

        key = f"{client_id}:{minute_key}"
        if key not in self.requests:
            self.requests[key] = 0

        self.requests[key] += 1

        old_key = f"{client_id}:{minute_key - 1}"
        self.requests.pop(old_key, None)

        return self.requests[key] <= self.requests_per_minute

    def clean_old_entries(self):
        """Clean old rate limit entries."""
        now = int(time.time() / 60)
        keys_to_remove = []
        for key in self.requests:
            minute = int(key.split(":")[1])
            if now - minute > 2:
                keys_to_remove.append(key)
        for key in keys_to_remove:
            self.requests.pop(key, None)


rate_limiter = RateLimiter(settings.RATE_LIMIT_PER_MINUTE)


async def rate_limit_middleware(request: Request, call_next: Callable):
    """Rate limiting middleware."""
    client_id = request.client.host if request.client else "unknown"

    if not rate_limiter.is_allowed(client_id):
        logger.warning(f"Rate limit exceeded for {client_id}")
        return JSONResponse(
            status_code=429, content={"error": "Rate limit exceeded", "retry_after": 60}
        )

    response = await call_next(request)
    return response


class CacheService:
    """Simple in-memory cache service."""

    def __init__(self):
        self.cache: dict = {}
        self.expiry: dict = {}

    def get(self, key: str) -> Optional[str]:
        """Get cached value."""
        if key in self.cache:
            if key in self.expiry and time.time() < self.expiry[key]:
                return self.cache[key]
            else:
                self.cache.pop(key, None)
                self.expiry.pop(key, None)
        return None

    def set(self, key: str, value: str, ttl: int = 300):
        """Set cached value."""
        self.cache[key] = value
        self.expiry[key] = time.time() + ttl

    def delete(self, key: str):
        """Delete cached value."""
        self.cache.pop(key, None)
        self.expiry.pop(key, None)

    def clear(self):
        """Clear all cache."""
        self.cache.clear()
        self.expiry.clear()


cache_service = CacheService()


async def cache_middleware(request: Request, call_next: Callable):
    """Caching middleware."""
    cache_key = request.url.path

    if request.method == "GET":
        cached = cache_service.get(cache_key)
        if cached:
            return JSONResponse(content=cached)

    response = await call_next(request)

    if request.method == "GET" and response.status_code == 200:
        try:
            import json

            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            cache_service.set(cache_key, body.decode(), ttl=60)
            response = JSONResponse(content=json.loads(body))
        except:
            pass

    return response
