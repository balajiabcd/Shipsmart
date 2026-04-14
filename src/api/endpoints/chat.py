from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
import uuid

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

try:
    from src.llm.router import create_router, get_status
    from src.llm.chat_interface import create_chat_interface
    from src.llm.prediction_integration import create_integrator

    LLM_AVAILABLE = True
except ImportError as e:
    logging.warning(f"LLM modules not available: {e}")
    LLM_AVAILABLE = False
    create_router = None
    create_chat_interface = None
    create_integrator = None
    get_status = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["AI Chat"])

conversations_store = {}


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
    if not LLM_AVAILABLE:
        return None

    if chat_interface is None:
        try:
            llm_router = create_router()
            chat_interface = create_chat_interface(llm_router)
            logger.info("Chat interface initialized")
        except Exception as e:
            logger.error(f"Error initializing chat: {e}")
            chat_interface = None
    return chat_interface


def get_integrator():
    global integrator, llm_router
    if not LLM_AVAILABLE:
        return None

    if integrator is None:
        try:
            llm_router = create_router()
            integrator = create_integrator(llm_router)
            logger.info("Prediction integrator initialized")
        except Exception as e:
            logger.error(f"Error initializing integrator: {e}")
            integrator = None
    return integrator


def _generate_fallback_response(message: str) -> str:
    """Generate a fallback response when LLM is not available"""
    message_lower = message.lower()

    if "delay" in message_lower:
        return "I can help you with delay predictions. Currently using demo mode. The system can predict delivery delays based on weather, traffic, distance, and driver performance factors."
    elif "route" in message_lower or "optimize" in message_lower:
        return "For route optimization, I can help find the fastest routes using Dijkstra's algorithm. Currently running in demo mode."
    elif "recommend" in message_lower:
        return "I can provide recommendations like rerouting, driver reassignment, or customer notifications based on delay predictions."
    elif "weather" in message_lower:
        return "Weather data can be integrated from OpenWeatherMap API to improve delay predictions."
    else:
        return f"I received your message: '{message}'. The AI chat feature is in demo mode. To enable full LLM capabilities, please set up Ollama or configure an OpenAI API key."


@router.post("/")
async def chat(request: ChatRequest):
    """Send a chat message and get response"""
    interface = get_chat_interface()

    if interface is None:
        conv_id = request.conversation_id or str(uuid.uuid4())
        response = _generate_fallback_response(request.message)
        return ChatResponse(
            conversation_id=conv_id,
            message=response,
            timestamp=datetime.now(),
        )

    try:
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
        conv_id = request.conversation_id or str(uuid.uuid4())
        return ChatResponse(
            conversation_id=conv_id,
            message=_generate_fallback_response(request.message),
            timestamp=datetime.now(),
        )


@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    interface = get_chat_interface()

    if interface is None:
        return {
            "conversation_id": conversation_id,
            "messages": [],
            "context": {},
            "note": "Running in demo mode",
        }

    try:
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
    interface = get_chat_interface()

    if interface is None:
        return {
            "status": "deleted",
            "conversation_id": conversation_id,
            "note": "demo mode",
        }

    try:
        interface.clear_conversation(conversation_id)
        return {"status": "deleted", "conversation_id": conversation_id}
    except Exception as e:
        return {"status": "deleted", "conversation_id": conversation_id, "note": str(e)}


@router.post("/explain")
async def explain_prediction(request: PredictionRequest):
    """Get ML prediction with LLM explanation"""
    intgr = get_integrator()

    if intgr is None:
        delay_prob = (
            0.3 + (request.weather_severity / 10) + (request.traffic_index / 10)
        )
        return {
            "delivery_id": request.delivery_id,
            "prediction": delay_prob,
            "explanation": f"Based on weather severity {request.weather_severity}/10 and traffic index {request.traffic_index}/10, this delivery has a {delay_prob:.0%} probability of delay. Run in demo mode.",
            "root_causes": [
                "Weather conditions",
                "Traffic congestion",
                "Distance factor",
            ],
            "confidence": "medium",
        }

    try:
        context = request.dict()
        result = intgr.predict(context)
        return result

    except Exception as e:
        logger.error(f"Prediction explanation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_llm_status():
    """Get LLM service status"""
    if not LLM_AVAILABLE:
        return {
            "service": "demo",
            "available": False,
            "message": "LLM not configured - running in demo mode",
        }

    try:
        status = get_status() if get_status else {}
        interface = get_chat_interface()

        return {
            "llm_status": status,
            "available": LLM_AVAILABLE,
            "active_conversations": len(interface.list_conversations())
            if interface
            else 0,
        }
    except Exception as e:
        logger.error(f"Status error: {e}")
        return {
            "error": str(e),
            "available": LLM_AVAILABLE,
            "note": "Running in fallback mode",
        }


@router.post("/new")
async def new_conversation(user_id: str = "default", context: dict = None):
    """Start a new conversation"""
    interface = get_chat_interface()

    if interface is None:
        conv_id = str(uuid.uuid4())
        return {"conversation_id": conv_id, "status": "created", "mode": "demo"}

    try:
        conv_id = interface.create_conversation(user_id, context or {})
        return {"conversation_id": conv_id, "status": "created"}
    except Exception as e:
        conv_id = str(uuid.uuid4())
        return {"conversation_id": conv_id, "status": "created", "mode": "fallback"}
