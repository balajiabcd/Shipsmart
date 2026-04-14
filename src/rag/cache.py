import hashlib
import json
import time
from typing import Optional, Dict, List
from collections import OrderedDict


class LRUCache:
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl
        self.timestamps = {}

    def _make_key(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()

    def get(self, query: str) -> Optional[Dict]:
        key = self._make_key(query)

        if key not in self.cache:
            return None

        if time.time() - self.timestamps[key] > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return None

        self.cache.move_to_end(key)
        return self.cache[key]

    def set(self, query: str, results: Dict):
        key = self._make_key(query)

        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.max_size:
                oldest = next(iter(self.cache))
                del self.cache[oldest]
                del self.timestamps[oldest]

        self.cache[key] = results
        self.timestamps[key] = time.time()

    def clear(self):
        self.cache.clear()
        self.timestamps.clear()

    def size(self) -> int:
        return len(self.cache)


class RedisCache:
    def __init__(self, redis_client=None):
        self.redis = redis_client

    def get(self, query: str) -> Optional[Dict]:
        if self.redis is None:
            return None
        key = f"rag:query:{hashlib.md5(query.encode()).hexdigest()}"
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def set(self, query: str, results: Dict, ttl: int = 3600):
        if self.redis is None:
            return
        key = f"rag:query:{hashlib.md5(query.encode()).hexdigest()}"
        self.redis.setex(key, ttl, json.dumps(results))

    def invalidate(self, pattern: str = "rag:query:*"):
        if self.redis is None:
            return
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)


class SemanticCache:
    def __init__(self, threshold: float = 0.9, embedding_model=None):
        self.threshold = threshold
        self.embedding_model = embedding_model
        self.cache = OrderedDict()
        self.embeddings = {}

    def _get_embedding(self, query: str) -> Optional[List[float]]:
        if self.embedding_model is None:
            return None
        return self.embedding_model.embed(query).tolist()

    def get(self, query: str) -> Optional[Dict]:
        query_emb = self._get_embedding(query)
        if query_emb is None:
            return None

        for cached_query, cached_result in self.cache.items():
            cached_emb = self.embeddings.get(cached_query)
            if cached_emb is None:
                continue

            similarity = self._cosine_similarity(query_emb, cached_emb)
            if similarity >= self.threshold:
                return cached_result

        return None

    def set(self, query: str, results: Dict):
        query_emb = self._get_embedding(query)
        if query_emb is None:
            return

        self.cache[query] = results
        self.embeddings[query] = query_emb

        if len(self.cache) > 1000:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
            if oldest in self.embeddings:
                del self.embeddings[oldest]

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        return dot / (norm_a * norm_b + 1e-8)


class CacheManager:
    def __init__(self, use_redis: bool = False, redis_client=None):
        self.lru_cache = LRUCache()
        self.redis_cache = RedisCache(redis_client) if use_redis else None
        self.semantic_cache = None

    def get(self, query: str) -> Optional[Dict]:
        result = self.lru_cache.get(query)
        if result is not None:
            return result

        if self.redis_cache:
            result = self.redis_cache.get(query)
            if result is not None:
                self.lru_cache.set(query, result)
                return result

        if self.semantic_cache:
            return self.semantic_cache.get(query)

        return None

    def set(self, query: str, results: Dict):
        self.lru_cache.set(query, results)

        if self.redis_cache:
            self.redis_cache.set(query, results)

        if self.semantic_cache:
            self.semantic_cache.set(query, results)

    def clear(self):
        self.lru_cache.clear()
        if self.redis_cache:
            self.redis_cache.invalidate()
        if self.semantic_cache:
            self.semantic_cache.cache.clear()


if __name__ == "__main__":
    cache = LRUCache(max_size=100, ttl=60)
    cache.set("test query", {"results": ["doc1", "doc2"]})
    print(f"Cache size: {cache.size()}")
