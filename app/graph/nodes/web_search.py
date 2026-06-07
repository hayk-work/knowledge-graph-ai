from app.config import RETRIEVAL_TOP_K
from app.graph.state import ContextItem, State
from app.mcp import tavily


def web_search_node(state: State) -> dict:
    query = state.get("rewritten_question") or state["question"]
    result = tavily.web_search(query)

    context: list[ContextItem] = []
    for item in result.get("results", [])[:RETRIEVAL_TOP_K]:
        content = item.get("content") or ""
        if not content:
            continue
        context.append(
            ContextItem(
                text=content,
                source=item.get("url") or item.get("title") or "tavily",
                score=float(item.get("score") or 0.0),
                origin="tavily",
            )
        )

    return {"context": context}
