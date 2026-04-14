import os
import requests
import json
import logging
from typing import Dict, List, Optional, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_ACTIVE_MODEL", "phi:2.7b")


class OllamaClient:
    def __init__(self, base_url: str = None, model: str = None):
        self.base_url = base_url or OLLAMA_BASE_URL
        self.model = model or DEFAULT_MODEL
        self.api_url = f"{self.base_url}/api"

    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> List[Dict]:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                return response.json().get("models", [])
            return []
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []

    def get_current_model(self) -> str:
        """Get the current model name"""
        return self.model

    def set_model(self, model: str):
        """Set the model to use"""
        self.model = model
        logger.info(f"Model set to: {model}")

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
        stream: bool = False,
    ) -> str:
        """Generate text from prompt"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                f"{self.api_url}/generate", json=payload, timeout=120
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                logger.error(
                    f"Generate error: {response.status_code} - {response.text}"
                )
                return f"Error: {response.status_code}"

        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"Error: {str(e)}"

    async def generate_async(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Async version of generate"""
        return self.generate(prompt, system_prompt, temperature, max_tokens)

    def chat(
        self, messages: List[Dict], temperature: float = 0.7, max_tokens: int = 500
    ) -> str:
        """Chat with conversation history"""

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }

        try:
            response = requests.post(f"{self.api_url}/chat", json=payload, timeout=120)

            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            else:
                logger.error(f"Chat error: {response.status_code}")
                return f"Error: {response.status_code}"

        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Error: {str(e)}"

    def embed(self, text: str) -> List[float]:
        """Get embeddings for text"""

        payload = {"model": self.model, "prompt": text}

        try:
            response = requests.post(
                f"{self.api_url}/embeddings", json=payload, timeout=30
            )

            if response.status_code == 200:
                return response.json().get("embedding", [])
            return []

        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return []


def create_client(model: str = None) -> OllamaClient:
    """Factory function to create Ollama client"""
    return OllamaClient(model=model)


def check_ollama_status() -> Dict:
    """Check Ollama status and available models"""
    client = OllamaClient()

    status = {
        "available": client.is_available(),
        "models": [],
        "current_model": client.get_current_model(),
    }

    if status["available"]:
        status["models"] = client.list_models()

    return status
