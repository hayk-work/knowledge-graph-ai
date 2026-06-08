from app.config import CHAT_SUMMARY_THRESHOLD
from app.graph.state import State
from app.llm.groq_client import invoke
from app.memory.history import format_history_for_prompt


def summarize_node(state: State) -> dict:
    history = state.get("chat_history", [])
    if len(history) <= CHAT_SUMMARY_THRESHOLD:
        return {}

    history_text = format_history_for_prompt(history, max_turns=len(history))
    prompt = f"""Summarize this conversation in 3-5 bullet points for future context.
Keep it concise and focused on decisions, facts, and user intent.

Conversation:
{history_text}

Summary:"""
    return {"conversation_summary": invoke(prompt).strip()}
