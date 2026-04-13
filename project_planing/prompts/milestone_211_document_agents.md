# Milestone #211: Document Agent Framework

**Your Role:** AI/LLM Engineer

Write agent framework documentation:

```markdown
# Shipsmart Agent Framework

## Overview

Multi-agent system using LangGraph, AutoGen, and MCP for intelligent delivery management.

## Architecture

### LangGraph Agents
- **State Management**: TypedDict-based state
- **Nodes**: Process, execute_tools, respond
- **Checkpointer**: MemorySaver for conversation persistence

### AutoGen Agents
- **Analyst**: Analyzes delay patterns
- **Recommender**: Suggests actions
- **Communicator**: Handles customer messages
- **Coordinator**: Orchestrates team

### MCP Tools
- `delivery_prediction` - Get delay probability
- `get_recommendations` - Get actionable recommendations
- `search_knowledge` - RAG-based search
- `delivery_status` - Current status
- `check_weather` - Weather information

## Fallback Strategy

1. Primary agent fails → retry up to 3 times
2. Retry fails → switch to fallback agent
3. Circuit breaker prevents repeated failures

## Usage

```python
orchestrator = AgentOrchestrator(agents)
result = await orchestrator.orchestrate({
    "intent": "delay_analysis",
    "delivery_id": "DEL001"
})
```

Save to `docs/agent_framework.md`. Commit.