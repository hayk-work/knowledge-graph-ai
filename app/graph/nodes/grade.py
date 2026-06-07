import json
import re

from app.config import RELEVANCE_THRESHOLD
from app.graph.state import State
from app.llm.groq_client import invoke
from app.prompts.grade import GRADE_CONTEXT_PROMPT


def _parse_grade_response(raw: str) -> tuple[float, str]:
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        return 0.0, "irrelevant"
    try:
        data = json.loads(match.group())
        score = float(data.get("score", 0.0))
        decision = data.get("decision", "irrelevant")
        if decision not in ("relevant", "irrelevant"):
            decision = "relevant" if score >= RELEVANCE_THRESHOLD else "irrelevant"
        return score, decision
    except (json.JSONDecodeError, TypeError, ValueError):
        return 0.0, "irrelevant"


def grade_node(state: State) -> dict:
    if not state["context"]:
        return {"relevance_score": 0.0, "relevance_decision": "irrelevant"}

    top_score = max(doc["score"] for doc in state["context"])
    if top_score < RELEVANCE_THRESHOLD:
        return {"relevance_score": top_score, "relevance_decision": "irrelevant"}

    documents = "\n\n".join(
        f"[{doc['source']}] (score: {doc['score']:.2f})\n{doc['text'][:400]}"
        for doc in state["context"][:3]
    )
    prompt = GRADE_CONTEXT_PROMPT.format(
        question=state["question"],
        documents=documents,
    )
    score, decision = _parse_grade_response(invoke(prompt))
    return {"relevance_score": score, "relevance_decision": decision}
