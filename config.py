import os

from dotenv import load_dotenv
from langchain_core.utils import secret_from_env
from pydantic import BaseModel, Field, SecretStr


load_dotenv()


class Config(BaseModel):
    llm_provider: str = os.getenv("LLM_PROVIDER", "ollama")
    llm_model: str = os.getenv("LLM_MODEL", "phi3")
    groq_api_key: SecretStr | None = Field(
        default_factory=secret_from_env("GROQ_API_KEY", default=None)
    )


config = Config()
