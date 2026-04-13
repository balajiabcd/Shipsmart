# Milestone #167: Set Up Ollama Locally

**Your Role:** AI/LLM Engineer

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

Commit a script `scripts/setup_ollama.sh` to automate setup.