from fastapi.testclient import TestClient

from app.graph.workflow import run_rag
from app.memory.checkpoint import delete_thread_checkpoint, get_checkpointer
from app.memory.history import append_turn, format_history_for_prompt
from main import app
from tests.conftest import EMPTY_PINECONE, make_llm_handler


def test_append_turn_and_trim_history():
    history = []
    history = append_turn(history, "What is LangGraph?", "A graph framework for LLM apps.")
    history = append_turn(history, "What about checkpoints?", "They persist graph state.")

    assert len(history) == 4
    formatted = format_history_for_prompt(history, max_turns=2)
    assert "User: What about checkpoints?" in formatted
    assert "Assistant: They persist graph state." in formatted
    assert "What is LangGraph?" not in formatted


def test_delete_thread_clears_checkpoint_data(isolated_checkpoint, mock_services):
    thread_id = "thread-delete-me"
    run_rag("What is LangGraph?", thread_id)

    checkpoint = get_checkpointer()
    config = {"configurable": {"thread_id": thread_id}}
    assert any(item.config["configurable"]["thread_id"] == thread_id for item in checkpoint.list(config))

    delete_thread_checkpoint(thread_id)

    assert not any(item.config["configurable"]["thread_id"] == thread_id for item in checkpoint.list(config))

    fresh = run_rag("New question after delete", thread_id)
    assert len(fresh["chat_history"]) == 2
    assert fresh["chat_history"][0]["content"] == "New question after delete"


def test_delete_thread_endpoint(mock_services, isolated_checkpoint):
    client = TestClient(app)
    created = client.post("/ask", json={"question": "What is LangGraph?"}).json()

    response = client.delete(f"/threads/{created['thread_id']}")
    body = response.json()

    assert response.status_code == 200
    assert body == {"deleted": True, "thread_id": created["thread_id"]}


def test_checkpoint_survives_new_run_with_same_thread(mock_services, isolated_checkpoint):
    mock_services["state"]["llm_handler"] = make_llm_handler(
        answer_prefix="Turn:",
        rewrite_map={
            "What is LangGraph?": "LangGraph overview",
            "What about Docker?": "Docker overview",
        },
    )
    def pinecone_by_topic(query: str, top_k: int = 5) -> dict:
        if query == "LangGraph overview":
            return {
                "query": query,
                "top_k": top_k,
                "matches": [
                    {
                        "score": 0.9,
                        "text": "LangGraph docs content",
                        "source": "langgraph/overview.md",
                    }
                ],
            }
        return EMPTY_PINECONE

    mock_services["state"]["pinecone_handler"] = pinecone_by_topic

    first = run_rag("What is LangGraph?", "thread-persist")
    second = run_rag("What about Docker?", "thread-persist")

    assert len(first["chat_history"]) == 2
    assert len(second["chat_history"]) == 4
    assert second["chat_history"][0]["content"] == "What is LangGraph?"
    assert second["context"][0]["origin"] == "tavily"
