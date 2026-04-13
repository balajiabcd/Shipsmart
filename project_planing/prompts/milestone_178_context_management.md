# Milestone #178: Implement Context Management

**Your Role:** AI/LLM Engineer

Maintain conversation state:

```python
# src/llm/context_manager.py

from datetime import datetime, timedelta
from typing import Optional, Dict
import json
import hashlib

class ContextManager:
    def __init__(self, redis_client=None, ttl_hours: int = 24):
        self.redis = redis_client
        self.ttl = timedelta(hours=ttl_hours)
        self.in_memory_context: Dict[str, dict] = {}
    
    def save_context(self, conversation_id: str, context: dict):
        """Save conversation context"""
        context["updated_at"] = datetime.now().isoformat()
        
        if self.redis:
            self.redis.set(
                f"context:{conversation_id}",
                json.dumps(context),
                ex=int(self.ttl.total_seconds())
            )
        else:
            self.in_memory_context[conversation_id] = context
    
    def get_context(self, conversation_id: str) -> Optional[dict]:
        """Retrieve conversation context"""
        if self.redis:
            data = self.redis.get(f"context:{conversation_id}")
            return json.loads(data) if data else None
        return self.in_memory_context.get(conversation_id)
    
    def update_context(self, conversation_id: str, updates: dict):
        """Update specific context fields"""
        context = self.get_context(conversation_id) or {}
        context.update(updates)
        context["updated_at"] = datetime.now().isoformat()
        self.save_context(conversation_id, context)
    
    def add_to_history(self, conversation_id: str, role: str, content: str):
        """Add message to conversation history"""
        context = self.get_context(conversation_id) or {"history": []}
        context["history"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 50 messages
        context["history"] = context["history"][-50:]
        self.save_context(conversation_id, context)
    
    def get_context_summary(self, conversation_id: str) -> str:
        """Get formatted context for LLM"""
        context = self.get_context(conversation_id)
        if not context:
            return "No previous context."
        
        history = context.get("history", [])
        recent = history[-5:] if history else []
        
        summary = "Previous conversation:\n"
        for msg in recent:
            summary += f"{msg['role']}: {msg['content'][:100]}...\n"
        
        return summary
    
    def clear_context(self, conversation_id: str):
        """Clear context when done"""
        if self.redis:
            self.redis.delete(f"context:{conversation_id}")
        else:
            self.in_memory_context.pop(conversation_id, None)
```

For production, use Redis. Commit.