from langchain_groq import ChatGroq

from app.config import GROQ_API_KEY, GROQ_MODEL

_llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL)


def invoke(prompt: str) -> str:
    response = _llm.invoke(prompt)
    return response.content
