import os


class LangChainSetup:
    def __init__(self):
        self.llms = {}

    def get_llm(self, model: str = None, **kwargs):
        try:
            from langchain_community.chat_models import ChatOllama

            return ChatOllama(
                model=model or os.getenv("OLLAMA_ACTIVE_MODEL", "phi:2.7b"),
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                **kwargs,
            )
        except ImportError:
            return None

    def create_chain(self, llm, prompt_template: str):
        try:
            from langchain.prompts import ChatPromptTemplate
            from langchain.chains import LLMChain

            prompt = ChatPromptTemplate.from_template(prompt_template)
            return LLMChain(llm=llm, prompt=prompt)
        except ImportError:
            return None


if __name__ == "__main__":
    setup = LangChainSetup()
    llm = setup.get_llm(os.getenv("OLLAMA_ACTIVE_MODEL", "phi:2.7b"))
    print(f"LangChain setup complete, LLM: {llm}")
