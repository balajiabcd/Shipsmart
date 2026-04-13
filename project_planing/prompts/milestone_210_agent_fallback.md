# Milestone #210: Create Agent Fallback Logic

**Your Role:** AI/LLM Engineer

Handle failures gracefully:

```python
# src/agents/fallback.py

from typing import Dict, Optional
import logging

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
                logger.warning(f"Agent {agent_name} failed: {e}")
                self.retry_count[agent_name] = self.retry_count.get(agent_name, 0) + 1
                
                # Try fallback
                if agent_name in self.fallback:
                    agent_name = self.fallback[agent_name]
                    continue
                else:
                    return self._create_error_response(str(e))
        
        return self._create_error_response("Max retries exceeded")
    
    async def _execute_task(self, agent_name: str, task: Dict) -> Dict:
        # Execute with appropriate agent
        agent = self.primary.get(agent_name) or self.fallback.get(agent_name)
        return {"result": "success", "agent": agent_name}
    
    def _create_error_response(self, error: str) -> Dict:
        return {
            "status": "error",
            "error": error,
            "fallback_used": False,
            "can_retry": True
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
            import time
            if time.time() - self.last_failure_time[agent_name] > self.timeout:
                self.failures[agent_name] = 0  # Reset
                return False
            return True
        return False
    
    def record_failure(self, agent_name: str):
        self.failures[agent_name] = self.failures.get(agent_name, 0) + 1
        import time
        self.last_failure_time[agent_name] = time.time()
    
    def record_success(self, agent_name: str):
        self.failures[agent_name] = 0
```

Commit.