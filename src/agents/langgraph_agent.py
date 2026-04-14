from typing import TypedDict, List, Dict


class AgentState(TypedDict):
    messages: List[Dict]
    delivery_context: Dict
    recommended_actions: List


class SimpleDeliveryAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.tools = []

    def add_tool(self, name: str, func: callable, description: str):
        self.tools.append({"name": name, "func": func, "description": description})

    async def process(self, input_data: Dict) -> Dict:
        messages = input_data.get("messages", [])

        if not messages:
            return {"response": "No messages provided"}

        last_message = messages[-1].get("content", "")

        response = {
            "response": f"Processed: {last_message}",
            "delivery_context": input_data.get("delivery_context", {}),
            "recommended_actions": [],
        }

        return response

    def should_continue(self, state: Dict) -> str:
        if state.get("recommended_actions"):
            return "continue"
        return "end"


def create_delivery_agent(llm=None, tools: List = None):
    return SimpleDeliveryAgent(llm)


if __name__ == "__main__":
    agent = create_delivery_agent()
    print("Delivery agent ready")
