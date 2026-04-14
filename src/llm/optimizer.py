import time
import hashlib
from typing import Optional, Dict, List, Any, Callable
from functools import wraps
import asyncio


class LLMOptimizer:
    def __init__(self, router):
        self.router = router
        self.metrics: Dict[str, List[float]] = {}

    async def optimized_generate(self, prompt: str, **kwargs) -> str:
        start_time = time.time()

        complexity = kwargs.pop("complexity", "medium")
        cache_response = kwargs.pop("cache", True)

        if cache_response:
            cached = self._get_cached_response(prompt)
            if cached:
                return cached

        response = await self.router.generate(prompt, complexity=complexity, **kwargs)

        if cache_response:
            self._cache_response(prompt, response)

        elapsed = time.time() - start_time
        self._record_metric(complexity, elapsed)

        return response

    def _get_cached_response(self, prompt: str) -> Optional[str]:
        cache_key = self._make_cache_key(prompt)
        return None

    def _cache_response(self, prompt: str, response: str):
        pass

    def _make_cache_key(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode()).hexdigest()

    def _record_metric(self, complexity: str, elapsed: float):
        if complexity not in self.metrics:
            self.metrics[complexity] = []
        self.metrics[complexity].append(elapsed)

    def get_performance_report(self) -> Dict[str, Dict[str, float]]:
        return {
            complexity: {
                "avg_time": sum(times) / len(times),
                "count": len(times),
                "min": min(times),
                "max": max(times),
            }
            for complexity, times in self.metrics.items()
        }


class ResponseCache:
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, str] = {}
        self.max_size = max_size
        self.access_order: List[str] = []

    def _make_key(self, prompt: str, model: str) -> str:
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        return f"{model}:{prompt_hash}"

    def get(self, prompt: str, model: str) -> Optional[str]:
        key = self._make_key(prompt, model)
        if key in self.cache:
            self.access_order.remove(key)
            self.access_order.append(key)
            return self.cache[key]
        return None

    def set(self, prompt: str, model: str, response: str):
        key = self._make_key(prompt, model)

        if key in self.cache:
            self.access_order.remove(key)
        elif len(self.cache) >= self.max_size:
            oldest = self.access_order.pop(0)
            del self.cache[oldest]

        self.cache[key] = response
        self.access_order.append(key)

    def clear(self):
        self.cache.clear()
        self.access_order.clear()

    def size(self) -> int:
        return len(self.cache)


async def stream_response(router, prompt: str):
    async for chunk in router.stream_generate(prompt):
        yield chunk


def timing_decorator(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        return result, elapsed

    return wrapper


class TokenOptimizer:
    def __init__(self, max_tokens: int = 2048):
        self.max_tokens = max_tokens

    def truncate_context(
        self, context: List[Dict[str, str]], max_messages: int = 10
    ) -> List[Dict[str, str]]:
        if len(context) <= max_messages:
            return context
        return context[-max_messages:]

    def summarize_history(
        self, history: List[Dict[str, str]], max_length: int = 500
    ) -> str:
        total_chars = sum(len(msg.get("content", "")) for msg in history)
        if total_chars <= max_length:
            return f"Conversation with {len(history)} messages."

        avg_per_msg = max_length // len(history)
        summaries = []
        for msg in history:
            content = msg.get("content", "")
            if len(content) > avg_per_msg:
                content = content[:avg_per_msg] + "..."
            summaries.append(content)

        return " | ".join(summaries)
