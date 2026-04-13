# Milestone #181: Optimize LLM Performance

**Your Role:** AI/LLM Engineer

Tune for speed and quality:

```python
# src/llm/optimizer.py

import time
from functools import wraps
from typing import Callable

class LLMOptimizer:
    def __init__(self, router):
        self.router = router
        self.metrics = {}
    
    async def optimized_generate(self, prompt: str, **kwargs):
        start_time = time.time()
        
        complexity = kwargs.pop("complexity", "medium")
        cache_response = kwargs.pop("cache", True)
        
        # Check cache
        if cache_response:
            cached = self._get_cached_response(prompt)
            if cached:
                return cached
        
        # Route to appropriate model
        response = await self.router.generate(prompt, complexity=complexity, **kwargs)
        
        # Cache response
        if cache_response:
            self._cache_response(prompt, response)
        
        # Record metrics
        elapsed = time.time() - start_time
        self._record_metric(complexity, elapsed)
        
        return response
    
    def _get_cached_response(self, prompt: str) -> str:
        # Simple hash-based cache (use Redis in production)
        cache_key = hash(prompt)
        return None  # Implement cache lookup
    
    def _cache_response(self, prompt: str, response: str):
        pass  # Implement cache storage
    
    def _record_metric(self, complexity: str, elapsed: float):
        if complexity not in self.metrics:
            self.metrics[complexity] = []
        self.metrics[complexity].append(elapsed)
    
    def get_performance_report(self) -> dict:
        return {
            complexity: {
                "avg_time": sum(times) / len(times),
                "count": len(times),
                "min": min(times),
                "max": max(times)
            }
            for complexity, times in self.metrics.items()
        }

# Caching strategies
class ResponseCache:
    def __init__(self, max_size: int = 1000):
        self.cache = {}
        self.max_size = max_size
    
    def _make_key(self, prompt: str, model: str) -> str:
        return f"{model}:{hash(prompt)}"
    
    def get(self, prompt: str, model: str) -> str:
        return self.cache.get(self._make_key(prompt, model))
    
    def set(self, prompt: str, model: str, response: str):
        if len(self.cache) >= self.max_size:
            # Remove oldest
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        
        self.cache[self._make_key(prompt, model)] = response

# Streaming for long responses
async def stream_response(router, prompt: str):
    async for chunk in router.stream_generate(prompt):
        yield chunk
```

Commit.