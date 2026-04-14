from typing import Dict, List


class AgentMemory:
    def __init__(self):
        self.checkpointer = None
        self.sessions = {}

    def create_checkpointer(self):
        try:
            from langgraph.checkpoint.memory import MemorySaver

            self.checkpointer = MemorySaver()
        except ImportError:
            self.checkpointer = None
        return self.checkpointer

    def create_conversation_memory(self):
        return {"chat_history": [], "return_messages": True}

    def create_vector_memory(self, vectorstore=None):
        return {"retriever": vectorstore, "memory_key": "context"}


class AgentStatePersistence:
    def __init__(self):
        self.sessions = {}

    def save_session(self, session_id: str, state: dict):
        self.sessions[session_id] = state

    def load_session(self, session_id: str) -> dict:
        return self.sessions.get(session_id, {})

    def clear_session(self, session_id: str):
        self.sessions.pop(session_id, None)

    def get_all_sessions(self) -> List[str]:
        return list(self.sessions.keys())


class ConversationManager:
    def __init__(self):
        self.history = {}

    def add_message(self, session_id: str, role: str, content: str):
        if session_id not in self.history:
            self.history[session_id] = []
        self.history[session_id].append({"role": role, "content": content})

    def get_history(self, session_id: str) -> List[Dict]:
        return self.history.get(session_id, [])

    def clear_history(self, session_id: str):
        if session_id in self.history:
            del self.history[session_id]


if __name__ == "__main__":
    memory = AgentMemory()
    print("Agent memory ready")
