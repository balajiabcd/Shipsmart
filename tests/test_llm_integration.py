import pytest
from src.llm.router import LLMRouter, create_router
from src.llm.prompts import PromptTemplates
from src.llm.system_prompts import get_system_prompt, list_available_roles
from src.llm.chat_interface import ChatInterface, create_chat_interface
from src.llm.ollama_client import OllamaClient, check_ollama_status


class TestOllamaClient:
    def test_client_creation(self):
        client = OllamaClient()
        assert client is not None
        assert client.base_url == "http://localhost:11434"

    def test_check_status(self):
        status = check_ollama_status()
        assert "available" in status


class TestLLMRouter:
    def test_router_creation(self):
        router = LLMRouter()
        assert router is not None

    def test_route_low_complexity(self):
        router = LLMRouter()
        route = router.route("general", complexity="low")
        assert route["provider"] == "ollama"

    def test_route_medium_complexity(self):
        router = LLMRouter()
        route = router.route("general", complexity="medium")
        assert route["provider"] == "ollama"

    def test_is_available(self):
        router = LLMRouter()
        status = router.is_available()
        assert isinstance(status, bool)


class TestPromptTemplates:
    def test_delay_explanation(self):
        pred = {
            "delay_probability": 0.75,
            "risk_level": "high",
            "top_factors": ["weather", "traffic"],
        }
        prompt = PromptTemplates.delay_explanation(pred)
        assert "75%" in prompt
        assert "weather" in prompt

    def test_customer_message(self):
        context = {"urgency": "high", "situation": "delay", "delay_minutes": 30}
        prompt = PromptTemplates.customer_message("DEL001", context)
        assert "DEL001" in prompt
        assert "30" in prompt

    def test_root_cause_analysis(self):
        factors = [
            {"feature": "weather", "impact": "high"},
            {"feature": "traffic", "impact": "medium"},
        ]
        context = {"weather": "rain", "traffic": "heavy", "driver_performance": "good"}
        prompt = PromptTemplates.root_cause_analysis(factors, context)
        assert "root causes" in prompt.lower()


class TestSystemPrompts:
    def test_get_default_prompt(self):
        prompt = get_system_prompt("default")
        assert "Shipsmart" in prompt

    def test_get_customer_service_prompt(self):
        prompt = get_system_prompt("customer_service")
        assert "Customer Service" in prompt

    def test_get_warehouse_prompt(self):
        prompt = get_system_prompt("warehouse_manager")
        assert "Warehouse" in prompt

    def test_get_explanation_prompt(self):
        prompt = get_system_prompt("explanation")
        assert "logistics" in prompt.lower()

    def test_list_roles(self):
        roles = list_available_roles()
        assert "default" in roles
        assert "customer_service" in roles
        assert len(roles) >= 6


class TestChatInterface:
    def test_create_conversation(self):
        router = create_router()
        interface = create_chat_interface(router)

        conv_id = interface.create_conversation("user123")

        assert conv_id is not None
        assert conv_id in interface.conversations

    def test_get_conversation(self):
        router = create_router()
        interface = create_chat_interface(router)

        conv_id = interface.create_conversation("user123")
        conv = interface.get_conversation(conv_id)

        assert conv is not None
        assert conv.conversation_id == conv_id

    def test_update_context(self):
        router = create_router()
        interface = create_chat_interface(router)

        conv_id = interface.create_conversation("user123")
        interface.update_context(conv_id, {"delivery_id": "DEL001"})

        conv = interface.get_conversation(conv_id)
        assert conv.context.get("delivery_id") == "DEL001"

    def test_intent_classification(self):
        router = create_router()
        interface = create_chat_interface(router)

        intent = interface._classify_intent("Why is my delivery late?")
        assert intent == "delay_inquiry"

        intent = interface._classify_intent("Suggest a better route")
        assert intent == "route_inquiry"

        intent = interface._classify_intent("Who is the driver?")
        assert intent == "driver_inquiry"


class TestContextManager:
    def test_save_and_get_context(self):
        from src.llm.context_manager import get_context_manager

        manager = get_context_manager()
        manager.save_context("test123", {"key": "value"})

        ctx = manager.get_context("test123")
        assert ctx is not None
        assert ctx["key"] == "value"

    def test_add_to_history(self):
        from src.llm.context_manager import get_context_manager

        manager = get_context_manager()
        manager.save_context("test123", {"history": []})
        manager.add_to_history("test123", "user", "Hello")

        ctx = manager.get_context("test123")
        assert len(ctx["history"]) == 1
        assert ctx["history"][0]["content"] == "Hello"

    def test_clear_context(self):
        from src.llm.context_manager import get_context_manager

        manager = get_context_manager()
        manager.save_context("test123", {"key": "value"})
        manager.clear_context("test123")

        ctx = manager.get_context("test123")
        assert ctx is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
