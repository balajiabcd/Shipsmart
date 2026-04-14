from typing import Dict, Callable, Any
import json


class MCPServer:
    def __init__(self, name: str = "shipsmart"):
        self.name = name
        self.tools = {}
        self._mcp_available = self._check_mcp()

    def _check_mcp(self):
        try:
            import mcp

            return True
        except ImportError:
            return False

    def register_tool(self, name: str, description: str, schema: dict, func: Callable):
        self.tools[name] = {"description": description, "schema": schema, "func": func}

    async def list_tools(self):
        return [
            {
                "name": name,
                "description": info["description"],
                "inputSchema": info["schema"],
            }
            for name, info in self.tools.items()
        ]

    async def call_tool(self, name: str, arguments: dict):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        func = self.tools[name]["func"]

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(**arguments)
            else:
                result = func(**arguments)
            return {"success": True, "result": result}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def run(self):
        print(f"MCP Server '{self.name}' ready with {len(self.tools)} tools")


import asyncio


def create_mcp_server(name: str = "shipsmart-delivery") -> MCPServer:
    return MCPServer(name)


if __name__ == "__main__":
    server = create_mcp_server()
    print(f"MCP server created: {server.name}, available: {server._mcp_available}")
