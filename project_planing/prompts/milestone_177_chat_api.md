# Milestone #177: Create /chat API Endpoint

**Your Role:** AI/LLM Engineer

Expose chat interface via API:

```python
# api/endpoints/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["AI Chat"])

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    user_id: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    timestamp: datetime

# In-memory store (use Redis in production)
chat_interface = None  # Initialize in main.py

@router.post("/")
async def chat(request: ChatRequest):
    global chat_interface
    
    try:
        if not request.conversation_id:
            request.conversation_id = chat_interface.create_conversation(
                request.user_id,
                request.context or {}
            )
        
        response = await chat_interface.get_response(
            request.conversation_id,
            request.message
        )
        
        return ChatResponse(
            conversation_id=request.conversation_id,
            message=response,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    conv = chat_interface.conversations.get(conversation_id)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conv.conversation_id,
        "messages": [
            {"role": m.role, "content": m.content, "timestamp": m.timestamp.isoformat()}
            for m in conv.messages
        ],
        "created_at": conv.created_at.isoformat()
    }

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    if conversation_id in chat_interface.conversations:
        del chat_interface.conversations[conversation_id]
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Conversation not found")
```

Add to `api/main.py`. Commit.