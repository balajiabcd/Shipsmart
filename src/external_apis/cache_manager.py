import json
import os
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Any, Optional, Dict

logger = logging.getLogger(__name__)


class APICache:
    def __init__(self, cache_dir: str = "cache/", ttl_hours: int = 1):
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_key(self, url: str, params: Optional[Dict] = None) -> str:
        """Generate a unique cache key from URL and params."""
        key = url + json.dumps(params, sort_keys=True)
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, url: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Get cached response if available and not expired."""
        cache_key = self._get_cache_key(url, params)
        filepath = os.path.join(self.cache_dir, f"{cache_key}.json")

        if os.path.exists(filepath):
            try:
                with open(filepath, "r") as f:
                    data = json.load(f)
                cached_time = datetime.fromisoformat(data["timestamp"])
                if cached_time + self.ttl > datetime.now():
                    logger.debug(f"Cache hit: {url}")
                    return data["response"]
                else:
                    logger.debug(f"Cache expired: {url}")
                    os.remove(filepath)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                logger.warning(f"Invalid cache file: {e}")
                os.remove(filepath)
        return None

    def set(self, url: str, params: Optional[Dict], response: Any) -> None:
        """Cache a response."""
        cache_key = self._get_cache_key(url, params)
        filepath = os.path.join(self.cache_dir, f"{cache_key}.json")

        try:
            with open(filepath, "w") as f:
                json.dump(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "url": url,
                        "params": params,
                        "response": response,
                    },
                    f,
                )
            logger.debug(f"Cached: {url}")
        except Exception as e:
            logger.error(f"Failed to cache response: {e}")

    def delete(self, url: str, params: Optional[Dict] = None) -> bool:
        """Delete a specific cache entry."""
        cache_key = self._get_cache_key(url, params)
        filepath = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def clear(self, pattern: Optional[str] = None) -> int:
        """Clear all cache or matching pattern."""
        count = 0
        for filename in os.listdir(self.cache_dir):
            if pattern is None or pattern in filename:
                os.remove(os.path.join(self.cache_dir, filename))
                count += 1
        logger.info(f"Cleared {count} cache files")
        return count

    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_size = 0
        file_count = 0
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
                file_count += 1
        return {
            "file_count": file_count,
            "total_size_bytes": total_size,
            "cache_dir": self.cache_dir,
            "ttl_hours": self.ttl.total_seconds() / 3600,
        }


_global_cache: Optional[APICache] = None


def get_cache() -> APICache:
    """Get the global cache instance."""
    global _global_cache
    if _global_cache is None:
        _global_cache = APICache()
    return _global_cache


class CachedAPI:
    """Mixin class to add caching to API clients."""

    def __init__(self, *args, cache_ttl: int = 1, **kwargs):
        self._cache = APICache(ttl_hours=cache_ttl)
        super().__init__(*args, **kwargs)

    def _get_cached_or_fetch(
        self, url: str, params: Optional[Dict] = None, use_cache: bool = True
    ):
        """Get from cache or fetch and cache."""
        if use_cache:
            cached = self._cache.get(url, params)
            if cached is not None:
                return cached
        return None


if __name__ == "__main__":
    cache = APICache(cache_dir="test_cache/", ttl_hours=1)
    cache.set("http://example.com/api", {"key": "value"}, {"data": "test"})
    result = cache.get("http://example.com/api", {"key": "value"})
    print(f"Cached result: {result}")
    print(f"Cache info: {cache.get_cache_info()}")
    cache.clear()
