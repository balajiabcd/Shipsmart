# Milestone #168: Pull Llama 3 Model

**Your Role:** AI/LLM Engineer

Download and configure Llama 3:

```bash
# Pull Llama 3 8B (requires ~4.7GB)
ollama pull llama3

# Or pull specifically sized model
ollama pull llama3:8b

# Verify
ollama list
```

Create configuration file:

```yaml
# config/llm_config.yaml
models:
  llama3:
    name: llama3
    size: 8b
    context_length: 8192
    use_cases:
      - complex_reasoning
      - detailed_explanations
      - code_generation
    priority: 2
```

Commit config.