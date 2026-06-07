from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    generate_node,
    grade_node,
    retrieve_node,
    rewrite_node,
    route_after_grade,
    web_search_node,
)
from app.graph.state import State

_graph = None


def build_graph():
    graph = StateGraph(State)
    graph.add_node("rewrite", rewrite_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_node)
    graph.add_node("web_search", web_search_node)
    graph.add_node("generate", generate_node)
    graph.add_edge(START, "rewrite")
    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("retrieve", "grade")
    graph.add_conditional_edges("grade", route_after_grade, {
        "generate": "generate",
        "web_search": "web_search",
    })
    graph.add_edge("web_search", "generate")
    graph.add_edge("generate", END)
    return graph.compile()


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def run_rag(question: str) -> State:
    graph = get_graph()
    return graph.invoke(
        {
            "question": question,
            "rewritten_question": "",
            "context": [],
            "relevance_score": 0.0,
            "relevance_decision": "",
            "answer": "",
        },
        config={
            "run_name": "knowledge-graph-rag",
            "tags": ["rag", "langgraph"],
            "metadata": {"project": "knowledge-graph-ai"},
        },
    )
