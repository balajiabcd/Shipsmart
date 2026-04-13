# Milestone #199: Set Up LangChain

**Your Role:** AI/LLM Engineer

Configure LangChain framework:

```bash
pip install langchain langchain-community langchain-openai langchain-anthropic
```

Create base setup:

```python
# src/agents/langchain_setup.py

from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
import os

class LangChainSetup:
    def __init__(self):
        self.llms = {}
    
    def get_llm(self, provider: str = "openai", model: str = None, **kwargs):
        if provider == "openai":
            return ChatOpenAI(
                model=model or "gpt-4",
                api_key=os.getenv("OPENAI_API_KEY"),
                **kwargs
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=model or "claude-3-5-sonnet-20241022",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                **kwargs
            )
        elif provider == "ollama":
            return ChatOllama(
                model=model or "mistral",
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            )
        
        raise ValueError(f"Unknown provider: {provider}")
    
    def create_chain(self, llm, prompt_template: str):
        from langchain.prompts import ChatPromptTemplate
        from langchain.chains import LLMChain
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        return LLMChain(llm=llm, prompt=prompt)
```

Test:
```python
setup = LangChainSetup()
llm = setup.get_llm("ollama", "mistral")
response = llm([HumanMessage(content="Hello")])
```

Commit.