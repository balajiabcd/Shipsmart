# Milestone #171: Configure OpenAI API

**Your Role:** AI/LLM Engineer

Set up OpenAI API access:

```bash
# Install OpenAI Python package
pip install openai
```

Create `.env` configuration:
```bash
# .env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_ORG=org-your-org-id
```

Create wrapper:

```python
# src/llm/openai_client.py
from openai import OpenAI
import os

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            organization=os.getenv("OPENAI_ORG")
        )
    
    def generate(self, prompt: str, model: str = "gpt-4", **kwargs):
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def chat(self, messages: list, model: str = "gpt-4", **kwargs):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
```

Test connection:
```python
client = OpenAIClient()
print(client.generate("Hello, what is 2+2?"))
```

Commit code and add to `.env.example`.