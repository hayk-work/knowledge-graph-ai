from app.graph.state import ContextItem


def extract_sources(context: list[ContextItem]) -> list[str]:
    seen: set[str] = set()
    sources: list[str] = []

    for doc in context:
        label = f"{doc['origin']}:{doc['source']}"
        if label not in seen:
            seen.add(label)
            sources.append(label)

    return sources
