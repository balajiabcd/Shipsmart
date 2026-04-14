from datetime import datetime, timedelta
from typing import Optional, Dict, List
import json
import logging

logger = logging.getLogger(__name__)


class ContextManager:
    def __init__(self, ttl_hours: int = 24):
        self.ttl = timedelta(hours=ttl_hours)
        self.in_memory_context: Dict[str, dict] = {}

    def save_context(self, conversation_id: str, context: dict):
        """Save conversation context"""
        context["updated_at"] = datetime.now().isoformat()
        self.in_memory_context[conversation_id] = context
        logger.info(f"Context saved for conversation {conversation_id}")

    def get_context(self, conversation_id: str) -> Optional[dict]:
        """Retrieve conversation context"""
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
        context["history"].append(
            {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
        )

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
            content = (
                msg["content"][:100] + "..."
                if len(msg["content"]) > 100
                else msg["content"]
            )
            summary += f"{msg['role']}: {content}\n"

        return summary

    def clear_context(self, conversation_id: str):
        """Clear context when done"""
        self.in_memory_context.pop(conversation_id, None)
        logger.info(f"Context cleared for conversation {conversation_id}")

    def get_delivery_context(self, conversation_id: str) -> Dict:
        """Get delivery-specific context"""
        context = self.get_context(conversation_id)
        if not context:
            return {}

        return context.get("delivery_context", {})

    def set_delivery_context(
        self, conversation_id: str, delivery_id: str, context: Dict
    ):
        """Set delivery-specific context"""
        ctx = self.get_context(conversation_id) or {}
        if "delivery_context" not in ctx:
            ctx["delivery_context"] = {}

        ctx["delivery_context"][delivery_id] = context
        self.save_context(conversation_id, ctx)

    def add_user_preference(self, conversation_id: str, key: str, value: any):
        """Add user preference to context"""
        ctx = self.get_context(conversation_id) or {}
        if "preferences" not in ctx:
            ctx["preferences"] = {}

        ctx["preferences"][key] = value
        self.save_context(conversation_id, ctx)

    def get_user_preference(self, conversation_id: str, key: str) -> Optional[any]:
        """Get user preference from context"""
        ctx = self.get_context(conversation_id)
        if not ctx:
            return None
        return ctx.get("preferences", {}).get(key)

    def get_all_conversations(self) -> List[str]:
        """Get all conversation IDs"""
        return list(self.in_memory_context.keys())

    def cleanup_expired(self):
        """Clean up expired contexts"""
        now = datetime.now()
        expired = []

        for conv_id, context in self.in_memory_context.items():
            updated = context.get("updated_at")
            if updated:
                updated_time = datetime.fromisoformat(updated)
                if now - updated_time > self.ttl:
                    expired.append(conv_id)

        for conv_id in expired:
            self.clear_context(conv_id)

        if expired:
            logger.info(f"Cleaned up {len(expired)} expired contexts")


context_manager = ContextManager()


def get_context_manager() -> ContextManager:
    return context_manager
