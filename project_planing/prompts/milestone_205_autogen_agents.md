# Milestone #205: Create AutoGen Agents

**Your Role:** AI/LLM Engineer

Define agent roles:

```python
# src/agents/autogen_agents.py

from .autogen_setup import AutoGenSetup

def create_delivery_team(llm_config):
    setup = AutoGenSetup()
    
    # Analyst Agent - analyzes delays
    analyst = setup.create_conversable_agent(
        name="analyst",
        system_message="""You are a logistics analyst. Analyze delivery delays and predict patterns.
        Use data from the prediction model and provide insights.""",
        llm_config=llm_config
    )
    
    # Recommender Agent - suggests actions
    recommender = setup.create_conversable_agent(
        name="recommender",
        system_message="""You are a delivery operations expert. Suggest actionable recommendations
        to prevent or mitigate delays. Consider rerouting, driver reassignment, slot changes.""",
        llm_config=llm_config
    )
    
    # Communicator Agent - handles customer
    communicator = setup.create_conversable_agent(
        name="communicator",
        system_message="""You are a customer service specialist. Generate friendly, clear messages
        to inform customers about their delivery status. Be empathetic and proactive.""",
        llm_config=llm_config
    )
    
    # Coordinator Agent - orchestrates team
    coordinator = setup.create_conversable_agent(
        name="coordinator",
        system_message="""You are the team coordinator. Integrate insights from analyst, 
        recommender, and communicator to provide complete delivery management.""",
        llm_config=llm_config
    )
    
    return {
        "analyst": analyst,
        "recommender": recommender,
        "communicator": communicator,
        "coordinator": coordinator
    }
```

Create group chat:
```python
agents = create_delivery_team(llm_config)
group = setup.create_group_chat(list(agents.values()))
manager = setup.create_manager(group, llm_config)
```

Commit.