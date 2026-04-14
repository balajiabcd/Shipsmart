import os


class AutoGenSetup:
    def __init__(self):
        self.agents = {}
        self._autogen_available = self._check_autogen()

    def _check_autogen(self):
        try:
            import autogen

            return True
        except ImportError:
            return False

    def create_llm_config(self):
        return {
            "model": os.getenv("OLLAMA_ACTIVE_MODEL", "phi:2.7b"),
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            "api_key": "ollama",
        }

    def create_conversable_agent(
        self, name: str, system_message: str, llm_config: dict
    ):
        if not self._autogen_available:
            return {
                "name": name,
                "system_message": system_message,
                "llm_config": llm_config,
            }

        try:
            from autogen import ConversableAgent

            return ConversableAgent(
                name=name,
                system_message=system_message,
                llm_config=llm_config,
                human_input_mode="NEVER",
                code_execution_config=False,
            )
        except Exception:
            return {
                "name": name,
                "system_message": system_message,
                "llm_config": llm_config,
            }

    def create_group_chat(self, agents: list, speaker_selection_method: str = "auto"):
        if not self._autogen_available:
            return {"agents": agents, "max_round": 10}

        try:
            from autogen import GroupChat

            return GroupChat(
                agents=agents,
                messages=[],
                max_round=10,
                speaker_selection_method=speaker_selection_method,
            )
        except Exception:
            return {"agents": agents, "max_round": 10}

    def create_manager(self, group_chat, llm_config: dict):
        if not self._autogen_available:
            return None

        try:
            from autogen import GroupChatManager

            return GroupChatManager(groupchat=group_chat, llm_config=llm_config)
        except Exception:
            return None


if __name__ == "__main__":
    setup = AutoGenSetup()
    config = setup.create_llm_config()
    print(f"AutoGen setup: available={setup._autogen_available}")
