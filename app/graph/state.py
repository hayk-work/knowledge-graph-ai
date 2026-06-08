from typing import TypedDict


class ContextItem(TypedDict):
    text: str
    source: str
    score: float
    origin: str


class ChatMessage(TypedDict):
    role: str
    content: str


class State(TypedDict):
    thread_id: str
    question: str
    rewritten_question: str
    chat_history: list[ChatMessage]
    conversation_summary: str
    context: list[ContextItem]
    relevance_score: float
    relevance_decision: str
    answer: str
