from typing import TypedDict, Annotated, List, Dict
import operator


class AgentState(TypedDict):
    messages: List[Dict]
    context: Dict
    next_action: str
    results: Dict


def create_agent_graph(llm):
    try:
        from langgraph.graph import StateGraph, END
        from langgraph.prebuilt import ToolNode

        graph = StateGraph(AgentState)

        graph.add_node("process", process_messages)
        graph.add_node("execute_tools", execute_tools)
        graph.add_node("respond", generate_response)

        graph.set_entry_point("process")
        graph.add_edge("process", "execute_tools")
        graph.add_edge("execute_tools", "respond")
        graph.add_edge("respond", END)

        return graph.compile()
    except ImportError:
        return None


async def process_messages(state: AgentState):
    if state.get("messages"):
        last_message = state["messages"][-1].get("content", "")
        state["context"] = state.get("context", {})
        state["context"]["intent"] = detect_intent(last_message)
    return state


async def execute_tools(state: AgentState):
    return state


async def generate_response(state: AgentState):
    return state


def detect_intent(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ["delay", "late", "predict"]):
        return "delay_prediction"
    elif any(w in text_lower for w in ["recommend", "suggest", "improve"]):
        return "recommendation"
    elif any(w in text_lower for w in ["status", "where", "tracking"]):
        return "status_check"
    return "general"


class LangGraphSetup:
    def __init__(self):
        self.graph = None

    def create_delivery_agent(self, llm, tools: List = None):
        self.graph = create_agent_graph(llm)
        return self.graph

    async def invoke(self, input_data: Dict):
        if self.graph:
            return await self.graph.ainvoke(input_data)
        return {"error": "Graph not initialized"}


if __name__ == "__main__":
    setup = LangGraphSetup()
    print("LangGraph setup ready")
