from typing import Dict, Optional
import requests
import os


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


class AgentTools:
    def __init__(self, api_base_url: str = None):
        self.api_base = api_base_url or API_BASE_URL

    def predict_delay(self, delivery_id: str, context: Dict = None) -> Dict:
        """Predict delay probability for a delivery"""
        try:
            response = requests.post(
                f"{self.api_base}/predict/",
                json={"delivery_id": delivery_id, "context": context or {}},
                timeout=10,
            )
            if response.status_code == 200:
                return response.json()
            return {"error": f"API returned {response.status_code}"}
        except Exception as e:
            return {"error": str(e), "delivery_id": delivery_id}

    def get_recommendations(
        self, delivery_id: str, max_recommendations: int = 5
    ) -> Dict:
        """Get actionable recommendations"""
        try:
            response = requests.post(
                f"{self.api_base}/recommend/",
                json={"delivery_id": delivery_id, "max": max_recommendations},
                timeout=10,
            )
            if response.status_code == 200:
                return response.json()
            return {"error": f"API returned {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def search_knowledge(self, query: str, top_k: int = 3) -> Dict:
        """Search knowledge base via RAG"""
        try:
            response = requests.post(
                f"{self.api_base}/rag/query",
                json={"query": query, "top_k": top_k},
                timeout=10,
            )
            if response.status_code == 200:
                return response.json()
            return {"results": [], "answer": "Service unavailable"}
        except Exception as e:
            return {"results": [], "answer": f"Error: {str(e)}"}

    def get_delivery_status(self, delivery_id: str) -> Dict:
        """Get current delivery status"""
        try:
            response = requests.get(
                f"{self.api_base}/deliveries/{delivery_id}", timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return {"status": "unknown", "delivery_id": delivery_id}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_weather_info(self, location: str, date: str = None) -> Dict:
        """Get weather information"""
        try:
            url = f"{self.api_base}/weather/{location}"
            if date:
                url += f"?date={date}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {"weather": "unknown", "location": location}
        except Exception as e:
            return {"weather": "error", "error": str(e)}


def create_tools() -> list:
    """Create list of available agent tools"""
    tools = AgentTools()

    return [
        {
            "name": "predict_delay",
            "func": tools.predict_delay,
            "description": "Predict delay probability for a delivery. Input: delivery_id, optional context",
        },
        {
            "name": "get_recommendations",
            "func": tools.get_recommendations,
            "description": "Get actionable recommendations for a delivery",
        },
        {
            "name": "search_knowledge",
            "func": tools.search_knowledge,
            "description": "Search the knowledge base for information",
        },
        {
            "name": "get_delivery_status",
            "func": tools.get_delivery_status,
            "description": "Get current status of a delivery",
        },
        {
            "name": "get_weather_info",
            "func": tools.get_weather_info,
            "description": "Get weather information for a location",
        },
    ]


if __name__ == "__main__":
    tools = AgentTools()
    print(f"Agent tools initialized with API: {tools.api_base}")
