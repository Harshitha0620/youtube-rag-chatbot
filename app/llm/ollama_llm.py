from langchain_ollama import (
    ChatOllama
)

from app.config import settings


_llm = None


def get_llm():

    global _llm

    if _llm is None:

        _llm = ChatOllama(
            model=settings.LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1
        )

    return _llm