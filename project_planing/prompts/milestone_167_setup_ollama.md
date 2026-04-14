# Milestone #167: Set Up Ollama Locally

**Status:** COMPLETED

**Your Role:** AI/LLM Engineer

**Instructions:**
Install and configure Ollama locally:

```bash
# Install Ollama
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows - Use WSL or download from https://ollama.com
```

Verify installation:
```bash
ollama --version
```

Start Ollama service:
```bash
ollama serve
```

In another terminal:
```bash
ollama list
```

**Completed:**
- Created `src/llm/ollama_client.py` with:
  - `OllamaClient` class - Connect to local Ollama API
  - `is_available()` - Check if Ollama is running
  - `list_models()` - List available models
  - `generate()` - Generate text from prompt
  - `chat()` - Chat with conversation history
  - `embed()` - Get embeddings
  - `check_ollama_status()` - Status helper

- Uses local Ollama at `http://localhost:11434`
- Default model from env or "llama3"

**Next Milestone:** Proceed to #173 - LLM Router

---

## Section 3: Instructions for Next AI Agent

Proceed to Milestone #173: Create LLM Router
- Route requests to appropriate model
- Handle fallbacks