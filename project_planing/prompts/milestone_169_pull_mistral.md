# Milestone #169: Pull Mistral Model

**Your Role:** AI/LLM Engineer

Download Mistral model:

```bash
ollama pull mistral

# Verify
ollama list
```

Update config:

```yaml
models:
  mistral:
    name: mistral
    size: 7b
    context_length: 8192
    use_cases:
      - general_purpose
      - fast_inference
      - efficient_reasoning
    priority: 1  # Good balance of speed and quality
```

Commit.