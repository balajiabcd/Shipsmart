# Milestone #207: Set Up MCP Server

**Your Role:** AI/LLM Engineer

Configure Model Context Protocol:

```bash
pip install mcp
```

Create MCP server:

```python
# src/agents/mcp_server.py

from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import asyncio

class MCPServer:
    def __init__(self, name: str = "shipsmart"):
        self.server = Server(name)
        self.tools = {}
        self._register_handlers()
    
    def _register_handlers(self):
        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(
                    name=name,
                    description=desc,
                    inputSchema=schema
                )
                for name, (desc, schema) in self.tools.items()
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name not in self.tools:
                raise ValueError(f"Unknown tool: {name}")
            
            func, _, _ = self.tools[name]
            result = await func(**arguments)
            
            return [TextContent(type="text", text=str(result))]
    
    def register_tool(self, name: str, description: str, schema: dict, func: callable):
        self.tools[name] = (func, description, schema)
    
    async def run(self):
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


# Example: Register MCP server tools
mcp = MCPServer("shipsmart-delivery")

mcp.register_tool(
    name="predict_delay",
    description="Predict delivery delay probability",
    schema={"delivery_id": {"type": "string"}},
    func=predict_delay
)

mcp.register_tool(
    name="get_recommendations",
    description="Get delay mitigation recommendations",
    schema={"delivery_id": {"type": "string"}},
    func=get_recommendations
)
```

Run: `python -m src.agents.mcp_server`. Commit.