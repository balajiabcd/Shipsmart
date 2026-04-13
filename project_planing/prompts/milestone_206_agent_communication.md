# Milestone #206: Configure Agent Communication

**Your Role:** AI/LLM Engineer

Set up inter-agent messaging:

```python
# src/agents/communication.py

from typing import Dict, List
import asyncio

class AgentCommunication:
    def __init__(self):
        self.message_queues: Dict[str, List[Dict]] = {}
        self.subscriptions: Dict[str, List[str]] = {}
    
    def subscribe(self, agent_id: str, channel: str):
        if channel not in self.subscriptions:
            self.subscriptions[channel] = []
        self.subscriptions[channel].append(agent_id)
    
    def publish(self, channel: str, message: Dict):
        if channel not in self.message_queues:
            self.message_queues[channel] = []
        self.message_queues[channel].append(message)
        
        # Notify subscribers
        for agent_id in self.subscriptions.get(channel, []):
            self._notify_agent(agent_id, message)
    
    def _notify_agent(self, agent_id: str, message: Dict):
        # In production, use async messaging (Redis, RabbitMQ)
        pass
    
    def get_messages(self, agent_id: str) -> List[Dict]:
        return self.message_queues.get(agent_id, [])


class MultiAgentOrchestrator:
    def __init__(self, agents: Dict, communication: AgentCommunication):
        self.agents = agents
        self.communication = communication
        self.workflows = {}
    
    async def run_workflow(self, workflow_name: str, initial_input: Dict):
        workflow = self.workflows.get(workflow_name)
        if not workflow:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        context = {"input": initial_input, "results": {}}
        
        for step in workflow:
            agent = self.agents[step["agent"]]
            prompt = step["prompt"].format(**context)
            
            response = await agent.generate(prompt)
            context["results"][step["name"]] = response
            
            # Publish to workflow channel
            self.communication.publish(f"workflow:{workflow_name}", {
                "step": step["name"],
                "result": response
            })
        
        return context["results"]
    
    def register_workflow(self, name: str, steps: List[Dict]):
        self.workflows[name] = steps
```

Commit.