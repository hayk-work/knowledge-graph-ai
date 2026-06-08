from fastapi.testclient import TestClient

from main import app


def test_ask_single_question_response_shape(mock_services, isolated_checkpoint):
    client = TestClient(app)

    response = client.post("/ask", json={"question": "What is LangGraph?"})
    body = response.json()

    assert response.status_code == 200
    assert body["answer"]
    assert body["thread_id"]
    assert body["sources"] == ["pinecone:langgraph/overview.md"]
    assert body["context"][0]["origin"] == "pinecone"
    assert body["context"][0]["source"] == "langgraph/overview.md"


def test_ask_reuses_thread_id_for_conversation(mock_services, isolated_checkpoint):
    client = TestClient(app)

    first = client.post("/ask", json={"question": "What is LangGraph?"}).json()
    second = client.post(
        "/ask",
        json={"question": "Tell me more.", "thread_id": first["thread_id"]},
    ).json()

    assert first["thread_id"] == second["thread_id"]
    assert "LangGraph" in second["answer"]


def test_ask_conversation_docs_then_tavily(mock_services, isolated_checkpoint):
    pinecone_calls = {"count": 0}

    def pinecone_switch(query: str, top_k: int = 5) -> dict:
        from tests.conftest import EMPTY_PINECONE, pinecone_with_docs

        pinecone_calls["count"] += 1
        if pinecone_calls["count"] == 1:
            return pinecone_with_docs(query, top_k)
        return EMPTY_PINECONE

    mock_services["state"]["pinecone_handler"] = pinecone_switch
    client = TestClient(app)

    first = client.post("/ask", json={"question": "What is LangGraph?"}).json()
    second = client.post(
        "/ask",
        json={"question": "And what about Docker 27?", "thread_id": first["thread_id"]},
    ).json()

    assert first["context"][0]["origin"] == "pinecone"
    assert second["context"][0]["origin"] == "tavily"
    assert first["thread_id"] == second["thread_id"]
    assert "LangGraph" in second["answer"]
    assert "Docker" in second["answer"]
    assert mock_services["calls"]["tavily"]


def test_ask_tavily_question_via_api(mock_services, isolated_checkpoint):
    mock_services["state"]["pinecone_handler"] = (
        lambda query, top_k=5: {"query": query, "top_k": top_k, "matches": []}
    )
    client = TestClient(app)

    response = client.post("/ask", json={"question": "What is the latest Docker release?"})
    body = response.json()

    assert response.status_code == 200
    assert body["context"][0]["origin"] == "tavily"
    assert mock_services["calls"]["tavily"]
