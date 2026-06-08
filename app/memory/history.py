from app.graph.state import ChatMessage


def append_turn(history: list[ChatMessage], question: str, answer: str) -> list[ChatMessage]:
    updated = list(history)
    updated.append({"role": "user", "content": question})
    updated.append({"role": "assistant", "content": answer})
    return updated


def format_history_for_prompt(history: list[ChatMessage], max_turns: int = 6) -> str:
    if not history:
        return "No prior conversation."

    trimmed = history[-max_turns:]
    lines = [f"{message['role'].capitalize()}: {message['content']}" for message in trimmed]
    return "\n".join(lines)
