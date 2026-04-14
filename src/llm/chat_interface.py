from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import uuid


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Optional[Dict] = None


@dataclass
class Conversation:
    conversation_id: str
    messages: List[Message] = field(default_factory=list)
    context: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class ChatInterface:
    def __init__(self, router, prompt_templates=None):
        self.router = router
        self.templates = prompt_templates
        self.conversations: Dict[str, Conversation] = {}

    def create_conversation(
        self, user_id: str = None, initial_context: Dict = None
    ) -> str:
        """Create a new conversation"""
        conv_id = str(uuid.uuid4())[:8]
        self.conversations[conv_id] = Conversation(
            conversation_id=conv_id,
            messages=[],
            context=initial_context or {},
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return conv_id

    def get_conversation(self, conv_id: str) -> Optional[Conversation]:
        """Get a conversation by ID"""
        return self.conversations.get(conv_id)

    def list_conversations(self) -> List[str]:
        """List all conversation IDs"""
        return list(self.conversations.keys())

    def add_message(self, conv_id: str, role: str, content: str, metadata: Dict = None):
        """Add a message to a conversation"""
        conv = self.conversations.get(conv_id)
        if conv:
            conv.messages.append(
                Message(
                    role=role,
                    content=content,
                    timestamp=datetime.now(),
                    metadata=metadata,
                )
            )
            conv.updated_at = datetime.now()

    def get_response(self, conv_id: str, user_message: str) -> str:
        """Get response from LLM"""
        conv = self.conversations.get(conv_id)
        if not conv:
            return "Conversation not found. Create one first."

        self.add_message(conv_id, "user", user_message)

        messages = self._build_messages(conv, user_message)

        response = self.router.chat(messages)

        self.add_message(conv_id, "assistant", response)

        return response

    def explain_delay(
        self,
        conv_id: str,
        delay_probability: float,
        top_factors: List[Dict],
        context: Dict,
    ) -> str:
        """Get delay explanation from LLM"""
        return self.router.explain_delay(delay_probability, top_factors, context)

    def get_recommendation(
        self, conv_id: str, delay_probability: float, context: Dict
    ) -> str:
        """Get recommendation from LLM"""
        return self.router.generate_recommendation(delay_probability, context)

    def answer_query(self, conv_id: str, question: str, context: Dict = None) -> str:
        """Answer logistics query"""
        return self.router.answer_logistics_query(question, context)

    def _build_messages(self, conv: Conversation, current_message: str) -> List[Dict]:
        """Build message list for LLM"""

        system_prompt = """You are ShipSmart's AI assistant for logistics operations. You help customer service agents, warehouse managers, and dispatchers with:
- Explaining delivery delays in simple terms
- Providing operational recommendations
- Answering questions about shipping policies
- Analyzing root causes of delivery issues

Be helpful, clear, and practical."""

        messages = [{"role": "system", "content": system_prompt}]

        for msg in conv.messages[-10:]:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": current_message})

        return messages

    def _classify_intent(self, message: str) -> str:
        """Classify user intent"""
        message_lower = message.lower()

        if any(w in message_lower for w in ["delay", "late", "problem", "why"]):
            return "delay_inquiry"
        if any(w in message_lower for w in ["route", "reroute", "alternative"]):
            return "route_inquiry"
        if any(w in message_lower for w in ["driver", "assign"]):
            return "driver_inquiry"
        if any(w in message_lower for w in ["recommend", "suggest", "action"]):
            return "recommendation"

        return "general"

    def update_context(self, conv_id: str, context: Dict):
        """Update conversation context"""
        conv = self.conversations.get(conv_id)
        if conv:
            conv.context.update(context)

    def clear_conversation(self, conv_id: str):
        """Clear conversation history"""
        if conv_id in self.conversations:
            del self.conversations[conv_id]

    def get_history(self, conv_id: str) -> List[Dict]:
        """Get conversation history"""
        conv = self.conversations.get(conv_id)
        if not conv:
            return []

        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in conv.messages
        ]


def create_chat_interface(router) -> ChatInterface:
    """Factory function to create chat interface"""
    return ChatInterface(router)
