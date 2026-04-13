# Milestone #173: Create LLM Routing Logic

**Your Role:** AI/LLM Engineer

Create intelligent model routing:

```python
# src/llm/router.py

from enum import Enum
from typing import Optional
import os

class ModelType(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class LLMRouter:
    def __init__(self, config_path: str = "config/llm_config.yaml"):
        self.config = self._load_config(config_path)
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    def _load_config(self, path: str) -> dict:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)
    
    def route(self, task_type: str, complexity: str = "medium") -> dict:
        """Route to appropriate model based on task"""
        
        if complexity == "low":
            return {
                "provider": ModelType.OLLAMA,
                "model": "phi3",
                "type": "fast"
            }
        
        if complexity == "high":
            if os.getenv("OPENAI_API_KEY"):
                return {
                    "provider": ModelType.OPENAI,
                    "model": "gpt-4",
                    "type": "high_quality"
                }
            elif os.getenv("ANTHROPIC_API_KEY"):
                return {
                    "provider": ModelType.ANTHROPIC,
                    "model": "claude-3-5-sonnet-20241022",
                    "type": "high_quality"
                }
        
        # Default to Ollama Mistral
        return {
            "provider": ModelType.OLLAMA,
            "model": "mistral",
            "type": "balanced"
        }
    
    async def generate(self, prompt: str, task_type: str = "general", **kwargs):
        route_info = self.route(task_type, kwargs.get("complexity", "medium"))
        
        if route_info["provider"] == ModelType.OLLAMA:
            return await self._ollama_generate(prompt, route_info["model"], **kwargs)
        elif route_info["provider"] == ModelType.OPENAI:
            return self._openai_generate(prompt, route_info["model"], **kwargs)
        elif route_info["provider"] == ModelType.ANTHROPIC:
            return self._anthropic_generate(prompt, route_info["model"], **kwargs)
    
    async def _ollama_generate(self, prompt: str, model: str, **kwargs):
        import aiohttp
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.ollama_base_url}/api/generate",
                json={"model": model, "prompt": prompt, **kwargs}
            ) as resp:
                return await resp.json()
```

Commit.