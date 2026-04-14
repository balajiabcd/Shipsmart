from .autogen_setup import AutoGenSetup


def create_delivery_team(llm_config):
    setup = AutoGenSetup()

    analyst = setup.create_conversable_agent(
        name="analyst",
        system_message="""You are a logistics analyst. Analyze delivery delays and predict patterns.
        Use data from the prediction model and provide insights.""",
        llm_config=llm_config,
    )

    recommender = setup.create_conversable_agent(
        name="recommender",
        system_message="""You are a delivery operations expert. Suggest actionable recommendations
        to prevent or mitigate delays. Consider rerouting, driver reassignment, slot changes.""",
        llm_config=llm_config,
    )

    communicator = setup.create_conversable_agent(
        name="communicator",
        system_message="""You are a customer service specialist. Generate friendly, clear messages
        to inform customers about their delivery status. Be empathetic and proactive.""",
        llm_config=llm_config,
    )

    coordinator = setup.create_conversable_agent(
        name="coordinator",
        system_message="""You are the team coordinator. Integrate insights from analyst, 
        recommender, and communicator to provide complete delivery management.""",
        llm_config=llm_config,
    )

    return {
        "analyst": analyst,
        "recommender": recommender,
        "communicator": communicator,
        "coordinator": coordinator,
    }


def create_group_chat(agents_dict, llm_config):
    setup = AutoGenSetup()
    agents = list(agents_dict.values())
    group = setup.create_group_chat(agents)
    manager = setup.create_manager(group, llm_config)
    return {"group": group, "manager": manager}


if __name__ == "__main__":
    import os

    config = {
        "model": os.getenv("OLLAMA_ACTIVE_MODEL", "phi:2.7b"),
        "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        "api_key": "ollama",
    }
    team = create_delivery_team(config)
    print(f"Delivery team created: {list(team.keys())}")
