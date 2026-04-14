import time
import logging
import requests
from functools import wraps
from typing import Callable, Any, Optional, Type, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class RetryStrategy(Enum):
    FIXED = "fixed"
    EXPONENTIAL = "exponential"
    LINEAR = "linear"


def retry_on_failure(
    max_retries: int = 3,
    backoff_factor: float = 2.0,
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL,
    exceptions: Tuple[Type[Exception], ...] = (
        requests.exceptions.RequestException,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
    ),
    on_retry: Optional[Callable] = None,
):
    """Decorator to retry a function on failure with exponential backoff."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt == max_retries - 1:
                        logger.error(
                            f"All {max_retries} attempts failed for {func.__name__}: {e}"
                        )
                        raise

                    if strategy == RetryStrategy.EXPONENTIAL:
                        wait_time = backoff_factor**attempt
                    elif strategy == RetryStrategy.LINEAR:
                        wait_time = backoff_factor * attempt
                    else:
                        wait_time = backoff_factor

                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying in {wait_time}s..."
                    )

                    if on_retry:
                        on_retry(attempt, e)

                    time.sleep(wait_time)

            if last_exception:
                raise last_exception
            return None

        return wrapper

    return decorator


class RobustAPI:
    """Base class for API clients with retry logic."""

    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    @retry_on_failure(max_retries=3, backoff_factor=2)
    def _make_request(
        self, method: str, url: str, **kwargs
    ) -> Optional[requests.Response]:
        """Make HTTP request with retry logic."""
        kwargs.setdefault("timeout", 10)
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response

    def get_with_retry(self, url: str, **kwargs) -> Optional[dict]:
        """GET request with retry."""
        response = self._make_request("GET", url, **kwargs)
        return response.json() if response else None

    def post_with_retry(self, url: str, **kwargs) -> Optional[dict]:
        """POST request with retry."""
        response = self._make_request("POST", url, **kwargs)
        return response.json() if response else None


class CircuitBreaker:
    """Circuit breaker pattern to prevent cascading failures."""

    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == "open":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "half-open"
                logger.info("Circuit breaker transitioning to half-open")
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = func(*args, **kwargs)
            if self.state == "half-open":
                self.state = "closed"
                self.failure_count = 0
                logger.info("Circuit breaker closed")
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "open"
                logger.error("Circuit breaker opened")

            raise


class FallbackHandler:
    """Handler for fallback data when API fails."""

    def __init__(self):
        self.fallback_data = {}

    def register_fallback(self, key: str, data: Any):
        """Register fallback data for a specific API."""
        self.fallback_data[key] = data

    def get_fallback(self, key: str) -> Optional[Any]:
        """Get fallback data."""
        return self.fallback_data.get(key)


_global_fallback = FallbackHandler()


def get_fallback_handler() -> FallbackHandler:
    """Get global fallback handler."""
    return _global_fallback


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    class TestAPI(RobustAPI):
        @retry_on_failure(max_retries=3, backoff_factor=2)
        def fetch_data(self):
            import random

            if random.random() > 0.7:
                raise requests.exceptions.ConnectionError("Random failure")
            return {"data": "success"}

    api = TestAPI()
    for i in range(5):
        try:
            result = api.fetch_data()
            print(f"Attempt {i + 1}: Success - {result}")
        except Exception as e:
            print(f"Attempt {i + 1}: Failed - {e}")
