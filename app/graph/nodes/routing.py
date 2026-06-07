from app.graph.state import State


def route_after_grade(state: State) -> str:
    if state["relevance_decision"] == "relevant":
        return "generate"
    return "web_search"
