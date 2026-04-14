import os
import logging
from typing import Dict, List, Optional, Any
from enum import Enum

from .ollama_client import OllamaClient, check_ollama_status

logger = logging.getLogger(__name__)


class TaskType(Enum):
    GENERAL = "general"
    EXPLANATION = "explanation"
    ANALYSIS = "analysis"
    SUMMARY = "summary"
    RECOMMENDATION = "recommendation"
    CHAT = "chat"


class Complexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LLMRouter:
    def __init__(self, default_model: str = None):
        self.default_model = default_model or os.environ.get(
            "OLLAMA_ACTIVE_MODEL", "phi:2.7b"
        )
        self.ollama_client = OllamaClient(model=self.default_model)
        self._validate_connection()

    def _validate_connection(self):
        """Validate Ollama connection"""
        if not self.ollama_client.is_available():
            logger.warning("Ollama not available. Some features may not work.")
        else:
            models = self.ollama_client.list_models()
            logger.info(f"Connected to Ollama. Available models: {len(models)}")

    def get_available_models(self) -> List[Dict]:
        """Get list of available models"""
        return self.ollama_client.list_models()

    def is_available(self) -> bool:
        """Check if LLM service is available"""
        return self.ollama_client.is_available()

    def route(self, task_type: str = "general", complexity: str = "medium") -> Dict:
        """Route to appropriate model based on task"""

        model_mapping = {
            "fast": "phi3",
            "balanced": self.default_model,
            "high_quality": "llama3:70b"
            if self._has_model("llama3:70b")
            else self.default_model,
        }

        if complexity == "low":
            model = "phi3" if self._has_model("phi3") else self.default_model
        elif complexity == "high":
            model = model_mapping.get("high_quality", self.default_model)
        else:
            model = self.default_model

        return {"provider": "ollama", "model": model, "type": complexity}

    def _has_model(self, model_name: str) -> bool:
        """Check if specific model is available"""
        models = self.get_available_models()
        return any(m.get("name", "") == model_name for m in models)

    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        task_type: str = "general",
        complexity: str = "medium",
        temperature: float = 0.7,
        max_tokens: int = 500,
    ) -> str:
        """Generate text using routed model"""

        route_info = self.route(task_type, complexity)
        self.ollama_client.set_model(route_info["model"])

        try:
            response = self.ollama_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return response
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return f"Error generating response: {str(e)}"

    def chat(self, messages: List[Dict], complexity: str = "medium") -> str:
        """Chat with conversation history"""

        route_info = self.route("chat", complexity)
        self.ollama_client.set_model(route_info["model"])

        try:
            response = self.ollama_client.chat(
                messages=messages, temperature=0.7, max_tokens=500
            )
            return response
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return f"Error in chat: {str(e)}"

    def explain_delay(
        self, delay_probability: float, top_factors: List[Dict], delivery_context: Dict
    ) -> str:
        """Generate human-readable delay explanation"""

        system_prompt = """You are a logistics expert explaining delivery delays to customer service representatives.
Be clear, concise, and helpful. Use simple terms."""

        prompt = f"""A delivery has {delay_probability:.0%} probability of being delayed.

Top contributing factors:
"""

        for factor in top_factors[:5]:
            prompt += f"- {factor.get('feature', 'Unknown')}: {factor.get('impact', 'impact unclear')}\n"

        prompt += f"""
Delivery details:
- Distance: {delivery_context.get("distance_km", "unknown")} km
- Weather: {delivery_context.get("weather_condition", "unknown")}
- Traffic level: {delivery_context.get("traffic_level", "unknown")}
- Driver performance: {delivery_context.get("driver_performance", "unknown")}

Explain this in simple terms for a customer service representative. Keep it under 3 sentences. Then suggest one practical action the company can take."""

        return self.generate(
            prompt, system_prompt, task_type="explanation", complexity="medium"
        )

    def generate_recommendation(self, delay_probability: float, context: Dict) -> str:
        """Generate actionable recommendation"""

        system_prompt = """You are a logistics operations assistant. Provide practical, actionable recommendations."""

        prompt = f"""Delivery delay probability: {delay_probability:.0%}

Current situation:
- Weather severity: {context.get("weather_severity", "N/A")}/10
- Traffic index: {context.get("traffic_index", "N/A")}/10
- Driver performance: {context.get("driver_performance", "N/A")}
- Distance: {context.get("distance_km", "N/A")} km

Provide exactly 3 specific recommendations in bullet point format. Keep each under 10 words."""

        return self.generate(
            prompt, system_prompt, task_type="recommendation", complexity="low"
        )

    def answer_logistics_query(self, question: str, context: Dict = None) -> str:
        """Answer logistics-related questions"""

        system_prompt = """You are a knowledgeable logistics assistant. Answer questions about delivery operations, delays, and shipping policies."""

        prompt = question

        if context:
            prompt += f"""

Context:
- Current delay probability: {context.get("delay_probability", "unknown")}
- Active deliveries: {context.get("active_deliveries", "unknown")}
- Weather conditions: {context.get("weather_condition", "unknown")}
"""

        return self.generate(
            prompt, system_prompt, task_type="chat", complexity="medium"
        )


def create_router(model: str = None) -> LLMRouter:
    """Factory function to create LLM router"""
    return LLMRouter(default_model=model)


def get_status() -> Dict:
    """Get LLM service status"""
    ollama_status = check_ollama_status()

    return {
        "service": "ollama",
        "available": ollama_status["available"],
        "models": ollama_status["models"],
        "default_model": ollama_status["current_model"],
    }
