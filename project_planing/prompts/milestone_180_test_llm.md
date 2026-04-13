# Milestone #180: Test LLM Responses

**Your Role:** AI/LLM Engineer

Validate LLM outputs:

```python
# tests/test_llm_integration.py

import pytest
from src.llm.router import LLMRouter
from src.llm.prompts import PromptTemplates

@pytest.fixture
def router():
    return LLMRouter()

@pytest.fixture
def templates():
    return PromptTemplates()

@pytest.mark.asyncio
async def test_ollama_connection(router):
    result = await router.generate("What is 2+2?", complexity="low")
    assert result is not None
    assert len(result) > 0

@pytest.mark.asyncio
async def test_prompt_templates(templates):
    pred = {"delay_probability": 0.75, "risk_level": "high", "top_factors": ["weather", "traffic"]}
    prompt = templates.delay_explanation(pred)
    assert "75%" in prompt
    assert "weather" in prompt

@pytest.mark.asyncio
async def test_routing_low_complexity(router):
    route = router.route("general", complexity="low")
    assert route["provider"].value == "ollama"
    assert route["model"] == "phi3"

@pytest.mark.asyncio
async def test_routing_high_complexity(router):
    route = router.route("complex_reasoning", complexity="high")
    assert route["type"] == "high_quality"

def test_system_prompts():
    from src.llm.system_prompts import get_system_prompt
    
    default = get_system_prompt("default")
    assert "Shipsmart" in default
    
    cs = get_system_prompt("customer_service")
    assert "Customer Service" in cs

def test_chat_interface_message_flow():
    from src.llm.chat_interface import ChatInterface
    
    interface = ChatInterface(router, templates)
    conv_id = interface.create_conversation("user123")
    
    assert conv_id is not None
    assert conv_id in interface.conversations
```

Run tests:
```bash
pytest tests/test_llm_integration.py -v
```

Commit tests.