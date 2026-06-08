from app.config import SEARCH_QUERY_MAX_LENGTH
from app.graph.state import State
from app.llm.groq_client import invoke
from app.memory.history import format_history_for_prompt
from app.prompts.rewrite import REWRITE_QUERY_PROMPT
from app.search.query import clamp_search_query


def _conversation_context(state: State) -> str:
    summary = state.get("conversation_summary", "").strip()
    history = format_history_for_prompt(state.get("chat_history", []))
    if summary:
        return f"Summary:\n{summary}\n\nRecent messages:\n{history}"
    return history


def rewrite_node(state: State) -> dict:
    prompt = REWRITE_QUERY_PROMPT.format(
        question=state["question"],
        history_or_summary=_conversation_context(state),
    )
    rewritten = invoke(prompt).strip() or state["question"]
    return {
        "rewritten_question": clamp_search_query(rewritten, SEARCH_QUERY_MAX_LENGTH),
    }
