from typing import TypedDict


class ContextItem(TypedDict):
    text: str
    source: str
    score: float
    origin: str


class State(TypedDict):
    question: str
    rewritten_question: str
    context: list[ContextItem]
    relevance_score: float
    relevance_decision: str
    answer: str
