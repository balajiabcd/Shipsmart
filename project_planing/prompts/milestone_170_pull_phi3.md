# Milestone #170: Pull Phi-3 Model

**Your Role:** AI/LLM Engineer

Download Phi-3 small model:

```bash
ollama pull phi3

# Or specific variant
ollama pull phi3:mini

# Verify
ollama list
```

Update config:

```yaml
models:
  phi3:
    name: phi3
    size: 3.8b
    context_length: 4096
    use_cases:
      - quick_responses
      - simple_queries
      - low_latency_tasks
    priority: 0  # Fastest model, use for simple tasks
```

Commit.