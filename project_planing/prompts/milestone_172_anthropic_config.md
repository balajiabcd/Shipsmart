# Milestone #172: Configure Anthropic API

**Your Role:** AI/LLM Engineer

Set up Anthropic Claude access:

```bash
pip install anthropic
```

Add to `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

Create client:

```python
# src/llm/anthropic_client.py
import anthropic
import os

class AnthropicClient:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    def generate(self, prompt: str, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        response = self.client.messages.create(
            model=model,
            max_tokens=kwargs.get("max_tokens", 1024),
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def chat(self, messages: list, model: str = "claude-3-5-sonnet-20241022", **kwargs):
        return self.client.messages.create(
            model=model,
            max_tokens=kwargs.get("max_tokens", 1024),
            messages=messages
        )
```

Test:
```python
client = AnthropicClient()
print(client.generate("Hello"))
```

Commit and update `.env.example`.