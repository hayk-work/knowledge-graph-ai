from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    generate_node,
    grade_node,
    retrieve_node,
    rewrite_node,
    route_after_grade,
    summarize_node,
    web_search_node,
)
from app.graph.state import State
from app.memory.checkpoint import get_checkpointer
from app.memory.history import append_turn

_graph = None


def build_graph():
    graph = StateGraph(State)
    graph.add_node("summarize", summarize_node)
    graph.add_node("rewrite", rewrite_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_node)
    graph.add_node("web_search", web_search_node)
    graph.add_node("generate", generate_node)
    graph.add_edge(START, "summarize")
    graph.add_edge("summarize", "rewrite")
    graph.add_edge("rewrite", "retrieve")
    graph.add_edge("retrieve", "grade")
    graph.add_conditional_edges("grade", route_after_grade, {
        "generate": "generate",
        "web_search": "web_search",
    })
    graph.add_edge("web_search", "generate")
    graph.add_edge("generate", END)
    return graph.compile(checkpointer=get_checkpointer())


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph


def run_rag(question: str, thread_id: str) -> State:
    graph = get_graph()
    state = graph.invoke(
        {
            "thread_id": thread_id,
            "question": question,
        },
        config={
            "configurable": {"thread_id": thread_id},
            "run_name": "knowledge-graph-rag",
            "tags": ["rag", "langgraph"],
            "metadata": {"project": "knowledge-graph-ai"},
        },
    )
    updated_history = append_turn(state.get("chat_history", []), question, state["answer"])
    state["chat_history"] = updated_history
    graph.update_state(
        {
            "configurable": {"thread_id": thread_id},
        },
        {"chat_history": updated_history},
    )
    return state
