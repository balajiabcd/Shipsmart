from typing import Dict, List
import asyncio


class AgentCommunication:
    def __init__(self):
        self.message_queues: Dict[str, List[Dict]] = {}
        self.subscriptions: Dict[str, List[str]] = {}

    def subscribe(self, agent_id: str, channel: str):
        if channel not in self.subscriptions:
            self.subscriptions[channel] = []
        if agent_id not in self.subscriptions[channel]:
            self.subscriptions[channel].append(agent_id)

    def publish(self, channel: str, message: Dict):
        if channel not in self.message_queues:
            self.message_queues[channel] = []
        self.message_queues[channel].append(message)

        for agent_id in self.subscriptions.get(channel, []):
            self._notify_agent(agent_id, message)

    def _notify_agent(self, agent_id: str, message: Dict):
        pass

    def get_messages(self, agent_id: str) -> List[Dict]:
        return self.message_queues.get(agent_id, [])

    def clear_channel(self, channel: str):
        if channel in self.message_queues:
            self.message_queues[channel] = []


class MultiAgentOrchestrator:
    def __init__(self, agents: Dict, communication: AgentCommunication = None):
        self.agents = agents
        self.communication = communication or AgentCommunication()
        self.workflows = {}

    async def run_workflow(self, workflow_name: str, initial_input: Dict):
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        context = {"input": initial_input, "results": {}}

        for step in workflow:
            agent = self.agents.get(step["agent"])
            if agent:
                prompt = step["prompt"].format(**context)
                context["results"][step["name"]] = f"Processed by {step['agent']}"

            self.communication.publish(
                f"workflow:{workflow_name}",
                {"step": step["name"], "result": context["results"].get(step["name"])},
            )

        return context["results"]

    def register_workflow(self, name: str, steps: List[Dict]):
        self.workflows[name] = steps

    def list_workflows(self) -> List[str]:
        return list(self.workflows.keys())


if __name__ == "__main__":
    comm = AgentCommunication()
    print("Agent communication ready")
