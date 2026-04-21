from langchain_core.language_models import BaseLanguageModel
from langchain_core.messages import AIMessage
from langchain_groq import ChatGroq
from langchain_ollama import OllamaLLM

from config import config


def create_llm(
    model: str | None = None, provider: str | None = None
) -> BaseLanguageModel:
    provider = provider or config.llm_provider
    model = model or config.llm_model

    if provider == "groq":
        if not config.groq_api_key:
            raise ValueError("GROQ_API_KEY must be set for the Groq LLM provider.")
        return ChatGroq(model=model, api_key=config.groq_api_key)

    return OllamaLLM(model=model)


def invoke_llm(llm: BaseLanguageModel, prompt: str) -> str:
    result = llm.invoke(prompt)
    return str(result.content) if isinstance(result, AIMessage) else result
