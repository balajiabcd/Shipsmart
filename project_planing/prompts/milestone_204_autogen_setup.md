# Milestone #204: Set Up AutoGen

**Your Role:** AI/LLM Engineer

Configure AutoGen multi-agent framework:

```bash
pip install pyautogen
```

Create setup:

```python
# src/agents/autogen_setup.py

import autogen
from autogen import ConversableAgent, GroupChat, GroupChatManager
import os

class AutoGenSetup:
    def __init__(self):
        self.agents = {}
    
    def create_llm_config(self, provider: str = "openai"):
        if provider == "openai":
            return {
                "model": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "temperature": 0.7
            }
        elif provider == "anthropic":
            return {
                "model": "claude-3-5-sonnet-20241022",
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "temperature": 0.7
            }
        elif provider == "ollama":
            return {
                "model": "mistral",
                "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                "api_key": "dummy"
            }
    
    def create_conversable_agent(self, name: str, system_message: str, llm_config: dict):
        return ConversableAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            human_input_mode="NEVER",
            code_execution_config=False
        )
    
    def create_group_chat(self, agents: list, speaker_selection_method: str = "auto"):
        return GroupChat(
            agents=agents,
            messages=[],
            max_round=10,
            speaker_selection_method=speaker_selection_method
        )
    
    def create_manager(self, group_chat: GroupChat, llm_config: dict):
        return GroupChatManager(
            groupchat=group_chat,
            llm_config=llm_config
        )
```

Test:
```python
setup = AutoGenSetup()
config = setup.create_llm_config("ollama")
agent = setup.create_conversable_agent("test", "You are a helpful assistant", config)
```

Commit.