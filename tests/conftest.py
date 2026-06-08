import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LANGGRAPH_DOC = {
    "score": 0.92,
    "text": "LangGraph is a library for building stateful multi-actor applications with LLMs.",
    "source": "langgraph/overview.md",
}

DOCKER_TAVILY_RESULT = {
    "results": [
        {
            "content": "Docker 27.0 was released with improved BuildKit caching.",
            "url": "https://example.com/docker-27",
            "title": "Docker 27 release notes",
            "score": 0.88,
        }
    ]
}

EMPTY_PINECONE = {"query": "", "top_k": 5, "matches": []}
LOW_SCORE_PINECONE = {
    "query": "",
    "top_k": 5,
    "matches": [{"score": 0.2, "text": "Unrelated content.", "source": "other.md"}],
}


def pinecone_with_docs(query: str, top_k: int = 5) -> dict:
    return {
        "query": query,
        "top_k": top_k,
        "matches": [LANGGRAPH_DOC],
    }


def make_llm_handler(
    *,
    grade_decision: str = "relevant",
    rewrite_map: dict[str, str] | None = None,
    answer_prefix: str = "Answer:",
):
    rewrite_map = rewrite_map or {}

    def invoke(prompt: str) -> str:
        if "grader assessing" in prompt:
            return f'{{"score": 0.9, "decision": "{grade_decision}"}}'

        if "Rewritten query:" in prompt and "Original query:" in prompt:
            original = prompt.split("Original query:")[-1].split("Rewritten query:")[0].strip()
            return rewrite_map.get(original, original)

        if "Summarize this conversation" in prompt:
            return "- User asked about LangGraph.\n- Assistant explained LangGraph basics."

        if "Answer the question using the context below." in prompt:
            if "langgraph/overview.md" in prompt.lower() or "langgraph is a library" in prompt.lower():
                return f"{answer_prefix} LangGraph is a stateful LLM workflow framework from docs."
            if "docker 27.0" in prompt.lower() or "example.com/docker-27" in prompt.lower():
                history = "Conversation history (recent):" in prompt
                if history and "langgraph" in prompt.lower():
                    return (
                        f"{answer_prefix} Earlier we discussed LangGraph from docs; "
                        "Docker 27.0 adds improved BuildKit caching per Tavily."
                    )
                return f"{answer_prefix} Docker 27.0 adds improved BuildKit caching per Tavily."

        return "mock-llm-response"

    return invoke


@pytest.fixture(autouse=True)
def reset_singletons():
    import app.graph.workflow as workflow
    import app.memory.checkpoint as checkpoint

    workflow._graph = None
    checkpoint._checkpointer = None
    yield
    workflow._graph = None
    checkpoint._checkpointer = None


@pytest.fixture
def isolated_checkpoint(tmp_path, monkeypatch):
    db_path = tmp_path / "checkpoints.db"
    monkeypatch.setenv("CHECKPOINT_DB_PATH", str(db_path))
    monkeypatch.setattr("app.config.CHECKPOINT_DB_PATH", str(db_path))
    monkeypatch.setattr("app.memory.checkpoint.CHECKPOINT_DB_PATH", str(db_path))
    return db_path


@pytest.fixture
def mock_services(monkeypatch):
    calls = {
        "pinecone": [],
        "tavily": [],
        "llm": [],
    }
    state = {
        "pinecone_handler": pinecone_with_docs,
        "tavily_handler": lambda query, max_results=None: DOCKER_TAVILY_RESULT,
        "llm_handler": make_llm_handler(),
    }

    def pinecone_run(query: str, top_k: int = 5) -> dict:
        calls["pinecone"].append({"query": query, "top_k": top_k})
        return state["pinecone_handler"](query, top_k)

    def tavily_search(query: str, max_results=None) -> dict:
        calls["tavily"].append({"query": query, "max_results": max_results})
        return state["tavily_handler"](query, max_results)

    def llm_invoke(prompt: str) -> str:
        calls["llm"].append(prompt)
        return state["llm_handler"](prompt)

    monkeypatch.setattr("app.mcp.pinecone.run", pinecone_run)
    monkeypatch.setattr("app.mcp.tavily.web_search", tavily_search)
    for target in (
        "app.llm.groq_client.invoke",
        "app.graph.nodes.rewrite.invoke",
        "app.graph.nodes.grade.invoke",
        "app.graph.nodes.summarize.invoke",
        "app.llm.rag.invoke",
    ):
        monkeypatch.setattr(target, llm_invoke)

    return {"calls": calls, "state": state}
