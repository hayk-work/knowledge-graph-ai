from app.config import RETRIEVAL_TOP_K
from app.graph.state import ContextItem, State
from app.mcp import pinecone


def retrieve_node(state: State) -> dict:
    query = state.get("rewritten_question") or state["question"]
    result = pinecone.run(query, top_k=RETRIEVAL_TOP_K)

    context: list[ContextItem] = []
    for match in result["matches"]:
        text = match.get("text")
        if not text:
            continue
        context.append(
            ContextItem(
                text=text,
                source=match.get("source") or "unknown",
                score=float(match.get("score") or 0.0),
                origin="pinecone",
            )
        )

    return {"context": context}
