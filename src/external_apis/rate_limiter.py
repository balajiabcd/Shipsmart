import time
import logging
from collections import defaultdict
from threading import Lock
from typing import Optional

logger = logging.getLogger(__name__)


class RateLimiter:
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.window_seconds = 60
        self.calls = defaultdict(list)
        self.lock = Lock()

    def acquire(self, key: str = "default") -> bool:
        """Try to acquire a token. Returns True if allowed, False if rate limit reached."""
        with self.lock:
            now = time.time()
            self.calls[key] = [
                t for t in self.calls[key] if now - t < self.window_seconds
            ]

            if len(self.calls[key]) >= self.calls_per_minute:
                return False

            self.calls[key].append(now)
            return True

    def wait_if_needed(self, key: str = "default") -> None:
        """Block until a token is available."""
        while not self.acquire(key):
            logger.debug(f"Rate limit reached for {key}, waiting...")
            time.sleep(1)

    def get_remaining(self, key: str = "default") -> int:
        """Get remaining calls available in current window."""
        with self.lock:
            now = time.time()
            self.calls[key] = [
                t for t in self.calls[key] if now - t < self.window_seconds
            ]
            return max(0, self.calls_per_minute - len(self.calls[key]))

    def reset(self, key: Optional[str] = None) -> None:
        """Reset rate limit for a specific key or all keys."""
        with self.lock:
            if key:
                self.calls[key] = []
            else:
                self.calls.clear()


_global_limiter = RateLimiter()


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    return _global_limiter


class RateLimitedAPI:
    """Mixin class to add rate limiting to API clients."""

    def __init__(self, *args, **kwargs):
        self._limiter = RateLimiter()
        super().__init__(*args, **kwargs)

    def _make_request_with_limit(
        self, method: str, url: str, key: str = "default", **kwargs
    ):
        """Make a request with rate limiting."""
        self._limiter.wait_if_needed(key)
        import requests

        return requests.request(method, url, **kwargs)


if __name__ == "__main__":
    limiter = RateLimiter(calls_per_minute=5)
    for i in range(10):
        result = limiter.acquire("test")
        print(f"Request {i + 1}: {'allowed' if result else 'blocked'}")
        remaining = limiter.get_remaining("test")
        print(f"  Remaining: {remaining}")
