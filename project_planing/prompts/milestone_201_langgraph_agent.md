# Milestone #201: Create LangGraph Agent

**Your Role:** AI/LLM Engineer

Build agent with tools:

```python
# src/agents/langgraph_agent.py

from langgraph.prebuilt import ToolNode
from langchain.tools import Tool
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    delivery_context: dict
    recommended_actions: list

def create_delivery_agent(llm):
    from langchain.agents import create_openai_functions_agent
    
    tools = [
        Tool.from_function(predict_delay, name="predict_delay", description="Predict delivery delay"),
        Tool.from_function(get_recommendations, name="get_recommendations", description="Get action recommendations"),
        Tool.from_function(search_knowledge, name="search_knowledge", description="Search knowledge base")
    ]
    
    agent = create_openai_functions_agent(llm, tools, prompt)
    
    # Build graph
    graph = StateGraph(AgentState)
    graph.add_node("agent", agent)
    graph.add_node("tools", ToolNode(tools))
    
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
    graph.add_edge("tools", "agent")
    
    return graph.compile()

def should_continue(state):
    if state.get("recommended_actions"):
        return "continue"
    return "end"
```

Commit.