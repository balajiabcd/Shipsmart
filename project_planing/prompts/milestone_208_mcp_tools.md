# Milestone #208: Create MCP Tools

**Your Role:** AI/LLM Engineer

Define MCP-enabled tools:

```python
# src/agents/mcp_tools.py

from .mcp_server import MCPServer
import requests

mcp = MCPServer("shipsmart-tools")

# Delivery Prediction Tool
mcp.register_tool(
    name="delivery_prediction",
    description="Get delay prediction for a specific delivery",
    schema={
        "delivery_id": {"type": "string", "description": "Unique delivery identifier"},
        "include_factors": {"type": "boolean", "description": "Include top contributing factors"}
    },
    func=lambda delivery_id, include_factors=True: requests.post(
        "http://localhost:8000/predict/",
        json={"delivery_id": delivery_id, "include_factors": include_factors}
    ).json()
)

# Recommendation Tool
mcp.register_tool(
    name="get_recommendations",
    description="Get actionable recommendations for a delivery",
    schema={
        "delivery_id": {"type": "string"},
        "max_recommendations": {"type": "integer", "default": 5}
    },
    func=lambda delivery_id, max_recommendations=5: requests.post(
        "http://localhost:8000/recommend/",
        json={"delivery_id": delivery_id, "max": max_recommendations}
    ).json()
)

# RAG Query Tool
mcp.register_tool(
    name="search_knowledge",
    description="Search delivery knowledge base",
    schema={
        "query": {"type": "string"},
        "top_results": {"type": "integer", "default": 3}
    },
    func=lambda query, top_results=3: requests.post(
        "http://localhost:8000/rag/query",
        json={"query": query, "top_k": top_results}
    ).json()
)

# Delivery Status Tool
mcp.register_tool(
    name="delivery_status",
    description="Get current status of a delivery",
    schema={"delivery_id": {"type": "string"}},
    func=lambda delivery_id: requests.get(
        f"http://localhost:8000/deliveries/{delivery_id}"
    ).json()
)

# Weather Check Tool
mcp.register_tool(
    name="check_weather",
    description="Check weather at destination",
    schema={
        "location": {"type": "string"},
        "date": {"type": "string"}
    },
    func=lambda location, date=None: requests.get(
        f"http://localhost:8000/weather/{location}",
        params={"date": date} if date else {}
    ).json()
)
```

Commit.