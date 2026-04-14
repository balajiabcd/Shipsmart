from typing import Dict, List
import asyncio


class AgentOrchestrator:
    def __init__(self, agents: Dict):
        self.agents = agents
        self.tasks = {}

    async def orchestrate(self, request: Dict) -> Dict:
        intent = request.get("intent", "general")

        if intent == "delay_analysis":
            return await self._handle_delay_analysis(request)
        elif intent == "delivery_optimization":
            return await self._handle_delivery_optimization(request)
        elif intent == "customer_communication":
            return await self._handle_customer_comm(request)

        return {"status": "unknown_intent", "message": f"Unknown intent: {intent}"}

    async def _handle_delay_analysis(self, request: Dict) -> Dict:
        delivery_id = request.get("delivery_id", "")

        prediction = await self._call_agent(
            "analyst", {"task": "predict", "delivery_id": delivery_id}
        )

        recommendations = await self._call_agent(
            "recommender", {"task": "recommend", "prediction": prediction}
        )

        return {
            "delivery_id": delivery_id,
            "prediction": prediction,
            "recommendations": recommendations,
            "status": "completed",
        }

    async def _handle_delivery_optimization(self, request: Dict) -> Dict:
        delivery_id = request.get("delivery_id", "")

        route_optimized = await self._call_agent(
            "coordinator", {"task": "optimize_route", "delivery_id": delivery_id}
        )

        return {
            "delivery_id": delivery_id,
            "route_optimized": route_optimized,
            "status": "completed",
        }

    async def _handle_customer_comm(self, request: Dict) -> Dict:
        delivery_id = request.get("delivery_id", "")
        message = request.get("message", "")

        response = await self._call_agent(
            "communicator",
            {"task": "notify", "delivery_id": delivery_id, "message": message},
        )

        return {
            "delivery_id": delivery_id,
            "notification_sent": True,
            "response": response,
            "status": "completed",
        }

    async def _call_agent(self, agent_name: str, context: Dict) -> Dict:
        agent = self.agents.get(agent_name)
        if not agent:
            return {"error": f"Agent {agent_name} not found"}

        return {"result": "success", "agent": agent_name, "context": context}

    async def parallel_execution(self, tasks: List[Dict]) -> List[Dict]:
        results = await asyncio.gather(*[self.orchestrate(task) for task in tasks])
        return results

    def register_agent(self, name: str, agent):
        self.agents[name] = agent

    def list_agents(self) -> List[str]:
        return list(self.agents.keys())


if __name__ == "__main__":
    orchestrator = AgentOrchestrator({})
    print("Agent orchestrator ready")
