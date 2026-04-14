import logging
import time
from typing import Dict, Optional


logger = logging.getLogger(__name__)


class AgentFallback:
    def __init__(self, primary_agents: Dict, fallback_agents: Dict):
        self.primary = primary_agents
        self.fallback = fallback_agents
        self.retry_count = {}
        self.max_retries = 3

    async def execute_with_fallback(self, task: Dict, preferred_agent: str) -> Dict:
        agent_name = preferred_agent

        for attempt in range(self.max_retries):
            try:
                result = await self._execute_task(agent_name, task)
                self.retry_count[agent_name] = 0
                return result

            except Exception as e:
                logger.warning(
                    f"Agent {agent_name} failed (attempt {attempt + 1}): {e}"
                )
                self.retry_count[agent_name] = self.retry_count.get(agent_name, 0) + 1

                if agent_name in self.fallback:
                    agent_name = self.fallback[agent_name]
                    continue
                else:
                    return self._create_error_response(str(e))

        return self._create_error_response("Max retries exceeded")

    async def _execute_task(self, agent_name: str, task: Dict) -> Dict:
        agent = self.primary.get(agent_name) or self.fallback.get(agent_name)
        if agent:
            return {"result": "success", "agent": agent_name}
        return {"result": "error", "error": f"Agent {agent_name} not found"}

    def _create_error_response(self, error: str) -> Dict:
        return {
            "status": "error",
            "error": error,
            "fallback_used": False,
            "can_retry": True,
        }


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failures = {}
        self.last_failure_time = {}

    def is_open(self, agent_name: str) -> bool:
        if agent_name not in self.failures:
            return False

        if self.failures[agent_name] >= self.failure_threshold:
            if time.time() - self.last_failure_time[agent_name] > self.timeout:
                self.failures[agent_name] = 0
                return False
            return True
        return False

    def record_failure(self, agent_name: str):
        self.failures[agent_name] = self.failures.get(agent_name, 0) + 1
        self.last_failure_time[agent_name] = time.time()

    def record_success(self, agent_name: str):
        self.failures[agent_name] = 0

    def get_status(self, agent_name: str) -> Dict:
        return {
            "failures": self.failures.get(agent_name, 0),
            "is_open": self.is_open(agent_name),
            "last_failure": self.last_failure_time.get(agent_name),
        }


class RetryPolicy:
    def __init__(
        self,
        max_retries: int = 3,
        backoff_multiplier: float = 2.0,
        initial_delay: float = 1.0,
    ):
        self.max_retries = max_retries
        self.backoff_multiplier = backoff_multiplier
        self.initial_delay = initial_delay

    def get_delay(self, attempt: int) -> float:
        return self.initial_delay * (self.backoff_multiplier**attempt)

    async def execute_with_retry(self, func, *args, **kwargs):
        last_error = None

        for attempt in range(self.max_retries):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    delay = self.get_delay(attempt)
                    logger.info(
                        f"Retrying after {delay}s (attempt {attempt + 1}/{self.max_retries})"
                    )
                    time.sleep(delay)

        raise last_error


if __name__ == "__main__":
    fallback = AgentFallback({}, {})
    cb = CircuitBreaker()
    print("Fallback logic ready")
