# Milestone #197: Build Caching Layer

**Your Role:** AI/LLM Engineer

Cache frequent queries:

```python
# src/rag/cache.py

import hashlib
import json
import time
from typing import Optional, Dict
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
        
        # Check TTL
        if time.time() - self.timestamps[key] > self.ttl:
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def set(self, query: str, results: Dict):
        key = self._make_key(query)
        
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.max_size:
                # Remove oldest
                oldest = next(iter(self.cache))
                del self.cache[oldest]
                del self.timestamps[oldest]
        
        self.cache[key] = results
        self.timestamps[key] = time.time()
    
    def clear(self):
        self.cache.clear()
        self.timestamps.clear()


class RedisCache:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    def get(self, query: str) -> Optional[Dict]:
        key = f"rag:query:{hashlib.md5(query.encode()).hexdigest()}"
        data = self.redis.get(key)
        return json.loads(data) if data else None
    
    def set(self, query: str, results: Dict, ttl: int = 3600):
        key = f"rag:query:{hashlib.md5(query.encode()).hexdigest()}"
        self.redis.setex(key, ttl, json.dumps(results))
```

Commit.