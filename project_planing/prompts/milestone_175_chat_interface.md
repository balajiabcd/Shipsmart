# Milestone #175: Build Chat Interface

**Your Role:** AI/LLM Engineer

Create conversation flow:

```python
# src/llm/chat_interface.py

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
import uuid

@dataclass
class Message:
    role: str  # system, user, assistant
    content: str
    timestamp: datetime
    metadata: Optional[dict] = None

@dataclass
class Conversation:
    conversation_id: str
    messages: List[Message]
    context: dict
    created_at: datetime
    updated_at: datetime

class ChatInterface:
    def __init__(self, router, prompt_templates):
        self.router = router
        self.templates = prompt_templates
        self.conversations = {}
    
    def create_conversation(self, user_id: str, initial_context: dict = None) -> str:
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = Conversation(
            conversation_id=conv_id,
            messages=[],
            context=initial_context or {},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        return conv_id
    
    def add_message(self, conv_id: str, role: str, content: str, metadata: dict = None):
        conv = self.conversations[conv_id]
        conv.messages.append(Message(
            role=role,
            content=content,
            timestamp=datetime.now(),
            metadata=metadata
        ))
        conv.updated_at = datetime.now()
    
    async def get_response(self, conv_id: str, user_message: str) -> str:
        conv = self.conversations[conv_id]
        
        self.add_message(conv_id, "user", user_message)
        
        # Build messages with context
        messages = self._build_messages(conv, user_message)
        
        # Route to appropriate model
        response = await self.router.generate(
            messages,
            task_type=self._classify_intent(user_message)
        )
        
        self.add_message(conv_id, "assistant", response)
        
        return response
    
    def _build_messages(self, conv: Conversation, current_message: str) -> List[dict]:
        messages = [{"role": "system", "content": self._get_system_prompt(conv.context)}]
        
        for msg in conv.messages[-10:]:  # Last 10 messages
            messages.append({"role": msg.role, "content": msg.content})
        
        return messages
    
    def _classify_intent(self, message: str) -> str:
        message_lower = message.lower()
        if any(w in message_lower for w in ['delay', 'late', 'problem']):
            return "delay_inquiry"
        if any(w in message_lower for w in ['route', 'reroute', 'alternative']):
            return "route_inquiry"
        if any(w in message_lower for w in ['driver', 'assign']):
            return "driver_inquiry"
        return "general"
    
    def _get_system_prompt(self, context: dict) -> str:
        return f"""You are Shipsmart AI Assistant, a logistics expert.
        You help with delivery predictions, recommendations, and customer inquiries.
        Current context: {context}"""
```

Commit.