from app.graph.state import State
from app.llm.groq_client import invoke
from app.prompts.rewrite import REWRITE_QUERY_PROMPT


def rewrite_node(state: State) -> dict:
    prompt = REWRITE_QUERY_PROMPT.format(question=state["question"])
    rewritten = invoke(prompt).strip()
    return {"rewritten_question": rewritten or state["question"]}
