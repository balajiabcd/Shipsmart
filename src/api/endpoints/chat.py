from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

from ..llm.router import create_router, get_status
from ..llm.chat_interface import create_chat_interface
from ..llm.prediction_integration import create_integrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["AI Chat"])


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None


class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    user_id: Optional[str] = "default"
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    conversation_id: str
    message: str
    timestamp: datetime


class PredictionRequest(BaseModel):
    delivery_id: str
    distance_km: float
    weather_severity: float
    traffic_index: float
    driver_performance: float
    warehouse_efficiency: float
    route_complexity: float
    is_holiday: bool = False
    is_weekend: bool = False
    hour_of_day: int = 12
    day_of_week: int = 1


chat_interface = None
llm_router = None
integrator = None


def get_chat_interface():
    global chat_interface, llm_router
    if chat_interface is None:
        try:
            llm_router = create_router()
            chat_interface = create_chat_interface(llm_router)
            logger.info("Chat interface initialized")
        except Exception as e:
            logger.error(f"Error initializing chat: {e}")
    return chat_interface


def get_integrator():
    global integrator, llm_router
    if integrator is None:
        try:
            llm_router = create_router()
            integrator = create_integrator(llm_router)
            logger.info("Prediction integrator initialized")
        except Exception as e:
            logger.error(f"Error initializing integrator: {e}")
    return integrator


@router.post("/")
async def chat(request: ChatRequest):
    """Send a chat message and get response"""
    try:
        interface = get_chat_interface()

        if not request.conversation_id:
            request.conversation_id = interface.create_conversation(
                request.user_id, request.context or {}
            )

        response = interface.get_response(request.conversation_id, request.message)

        return ChatResponse(
            conversation_id=request.conversation_id,
            message=response,
            timestamp=datetime.now(),
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    try:
        interface = get_chat_interface()
        conv = interface.get_conversation(conversation_id)

        if not conv:
            raise HTTPException(status_code=404, detail="Conversation not found")

        return {
            "conversation_id": conv.conversation_id,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp.isoformat(),
                }
                for m in conv.messages
            ],
            "created_at": conv.created_at.isoformat(),
            "context": conv.context,
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    try:
        interface = get_chat_interface()
        interface.clear_conversation(conversation_id)
        return {"status": "deleted", "conversation_id": conversation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/explain")
async def explain_prediction(request: PredictionRequest):
    """Get ML prediction with LLM explanation"""
    try:
        intgr = get_integrator()

        context = request.dict()
        result = intgr.predict(context)

        return result

    except Exception as e:
        logger.error(f"Prediction explanation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_llm_status():
    """Get LLM service status"""
    try:
        status = get_status()
        interface = get_chat_interface()

        return {
            "llm_status": status,
            "active_conversations": len(interface.list_conversations())
            if interface
            else 0,
        }
    except Exception as e:
        logger.error(f"Status error: {e}")
        return {"error": str(e)}


@router.post("/new")
async def new_conversation(user_id: str = "default", context: dict = None):
    """Start a new conversation"""
    try:
        interface = get_chat_interface()
        conv_id = interface.create_conversation(user_id, context or {})

        return {"conversation_id": conv_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
