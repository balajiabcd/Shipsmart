import os
import requests
from .mcp_server import create_mcp_server


API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def create_delivery_tools():
    mcp = create_mcp_server("shipsmart-tools")

    def delivery_prediction(delivery_id: str, include_factors: bool = True):
        try:
            resp = requests.post(
                f"{API_BASE_URL}/predict/",
                json={"delivery_id": delivery_id},
                timeout=10,
            )
            return (
                resp.json()
                if resp.status_code == 200
                else {"error": "Service unavailable"}
            )
        except:
            return {"delivery_id": delivery_id, "delay_probability": 0.5}

    def get_recommendations(delivery_id: str, max_recommendations: int = 5):
        try:
            resp = requests.post(
                f"{API_BASE_URL}/recommend/",
                json={"delivery_id": delivery_id},
                timeout=10,
            )
            return resp.json() if resp.status_code == 200 else []
        except:
            return []

    def search_knowledge(query: str, top_results: int = 3):
        try:
            resp = requests.post(
                f"{API_BASE_URL}/rag/query", json={"query": query}, timeout=10
            )
            return resp.json() if resp.status_code == 200 else {"results": []}
        except:
            return {"results": [], "answer": "Service unavailable"}

    def delivery_status(delivery_id: str):
        try:
            resp = requests.get(f"{API_BASE_URL}/deliveries/{delivery_id}", timeout=10)
            return resp.json() if resp.status_code == 200 else {"status": "unknown"}
        except:
            return {"status": "unknown", "delivery_id": delivery_id}

    def check_weather(location: str, date: str = None):
        try:
            url = f"{API_BASE_URL}/weather/{location}"
            resp = requests.get(url, timeout=10)
            return resp.json() if resp.status_code == 200 else {"weather": "unknown"}
        except:
            return {"weather": "unknown", "location": location}

    mcp.register_tool(
        name="delivery_prediction",
        description="Get delay prediction for a specific delivery",
        schema={
            "delivery_id": {"type": "string"},
            "include_factors": {"type": "boolean"},
        },
        func=delivery_prediction,
    )

    mcp.register_tool(
        name="get_recommendations",
        description="Get actionable recommendations for a delivery",
        schema={
            "delivery_id": {"type": "string"},
            "max_recommendations": {"type": "integer"},
        },
        func=get_recommendations,
    )

    mcp.register_tool(
        name="search_knowledge",
        description="Search delivery knowledge base",
        schema={"query": {"type": "string"}, "top_results": {"type": "integer"}},
        func=search_knowledge,
    )

    mcp.register_tool(
        name="delivery_status",
        description="Get current status of a delivery",
        schema={"delivery_id": {"type": "string"}},
        func=delivery_status,
    )

    mcp.register_tool(
        name="check_weather",
        description="Check weather at destination",
        schema={"location": {"type": "string"}, "date": {"type": "string"}},
        func=check_weather,
    )

    return mcp


if __name__ == "__main__":
    mcp = create_delivery_tools()
    print(f"MCP tools registered: {list(mcp.tools.keys())}")
