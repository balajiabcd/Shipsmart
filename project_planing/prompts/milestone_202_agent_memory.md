# Milestone #202: Add Memory to Agent

**Your Role:** AI/LLM Engineer

Add conversation memory:

```python
# src/agents/memory.py

from langgraph.checkpoint.memory import MemorySaver
from langchain.memory import ConversationBufferMemory, VectorStoreRetrieverMemory
from langchain_community.vectorstores import Chroma

class AgentMemory:
    def __init__(self):
        self.checkpointer = MemorySaver()
    
    def create_checkpointer(self):
        return self.checkpointer
    
    def create_conversation_memory(self):
        return ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output",
            input_key="input"
        )
    
    def create_vector_memory(self, vectorstore):
        return VectorStoreRetrieverMemory(
            retriever=vectorstore.as_retriever(),
            memory_key="context"
        )


# For persisting agent state
class AgentStatePersistence:
    def __init__(self):
        self.sessions = {}
    
    def save_session(self, session_id: str, state: dict):
        self.sessions[session_id] = state
    
    def load_session(self, session_id: str) -> dict:
        return self.sessions.get(session_id, {})
    
    def clear_session(self, session_id: str):
        self.sessions.pop(session_id, None)
```

Use with agent:
```python
graph = create_agent_graph(llm).compile(checkpointer=memory.checkpointer)
```

Commit.