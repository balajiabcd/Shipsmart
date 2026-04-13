# Milestone #182: Document LLM Integration

**Your Role:** AI/LLM Engineer

Write AI assistant documentation:

```markdown
# Shipsmart LLM Integration

## Overview

Shipsmart uses multiple LLM providers for AI-powered assistance:
- **Ollama** (local): Phi-3, Mistral, Llama 3
- **OpenAI**: GPT-4
- **Anthropic**: Claude 3.5 Sonnet

## Architecture

### Components

1. **LLM Router** (`src/llm/router.py`)
   - Routes requests to appropriate model
   - Based on complexity and task type
   - Fallback logic for failures

2. **Chat Interface** (`src/llm/chat_interface.py`)
   - Manages conversations
   - Maintains message history
   - Intent classification

3. **Prompt Templates** (`src/llm/prompts.py`)
   - Predefined prompts for different use cases
   - Delay explanations
   - Recommendations
   - Customer messages

4. **Context Manager** (`src/llm/context_manager.py`)
   - Stores conversation context
   - Uses Redis for production

5. **System Prompts** (`src/llm/system_prompts.py`)
   - Role-based behavior definitions
   - Customer service, warehouse manager, etc.

## API Endpoints

- POST /chat/ - Send message
- GET /chat/{conv_id} - Get conversation
- DELETE /chat/{conv_id} - Delete conversation

## Model Selection

| Complexity | Model | Provider |
|------------|-------|----------|
| Low | Phi-3 | Ollama |
| Medium | Mistral | Ollama |
| High | GPT-4 / Claude | OpenAI / Anthropic |

## Usage Example

```python
response = await client.post("/chat/", json={
    "message": "Why is my delivery late?",
    "user_id": "user123"
})
```

## Testing

See `tests/test_llm_integration.py`
```

Save to `docs/llm_integration.md`. Commit.