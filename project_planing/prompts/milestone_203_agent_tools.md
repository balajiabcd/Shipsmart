# Milestone #203: Create Agent Tools

**Your Role:** AI/LLM Engineer

Define available actions:

```python
# src/agents/tools.py

from langchain.tools import Tool
import joblib
import pandas as pd
import requests

def predict_delay(delivery_id: str, context: dict = None) -> dict:
    """Predict delay probability for a delivery"""
    model = joblib.load('models/best_classifier.pkl')
    
    features = extract_features_for_delivery(delivery_id)
    if context:
        features.update(context)
    
    prob = model.predict_proba([features])[0]
    return {
        "delivery_id": delivery_id,
        "delay_probability": float(prob[1]),
        "on_time_probability": float(prob[0])
    }

def get_recommendations(delivery_id: str, delay_prob: float) -> dict:
    """Get actionable recommendations"""
    # Call recommendation API
    response = requests.post(
        "http://localhost:8000/recommend/",
        json={"delivery_id": delivery_id}
    )
    return response.json()

def search_knowledge(query: str) -> str:
    """Search knowledge base via RAG"""
    # Call RAG endpoint
    response = requests.post(
        "http://localhost:8000/rag/query",
        json={"query": query}
    )
    return response.json().get("answer", "No results found")

def get_delivery_status(delivery_id: str) -> dict:
    """Get current delivery status"""
    # Query database
    return db.get_delivery(delivery_id)

def get_weather_info(location: str) -> dict:
    """Get weather information"""
    # Call weather API
    return weather_api.get_current(location)

# Create LangChain tools
def create_tools():
    return [
        Tool(
            name="predict_delay",
            func=lambda d, c=None: predict_delay(d, c),
            description="Predict delay probability. Input: delivery_id, optional context"
        ),
        Tool(
            name="get_recommendations",
            func=get_recommendations,
            description="Get actionable recommendations for a delivery"
        ),
        Tool(
            name="search_knowledge",
            func=search_knowledge,
            description="Search the knowledge base for information"
        ),
        Tool(
            name="get_delivery_status",
            func=get_delivery_status,
            description="Get current status of a delivery"
        )
    ]
```

Commit.