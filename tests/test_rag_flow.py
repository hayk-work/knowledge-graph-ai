from app.graph.workflow import run_rag
from tests.conftest import EMPTY_PINECONE, LOW_SCORE_PINECONE, make_llm_handler, pinecone_with_docs


def test_single_question_uses_docs_not_tavily(mock_services, isolated_checkpoint):
    result = run_rag("What is LangGraph?", "thread-single")

    assert "LangGraph" in result["answer"]
    assert "docs" in result["answer"].lower() or "framework" in result["answer"].lower()
    assert len(result["context"]) == 1
    assert result["context"][0]["origin"] == "pinecone"
    assert result["context"][0]["source"] == "langgraph/overview.md"
    assert mock_services["calls"]["pinecone"]
    assert mock_services["calls"]["tavily"] == []
    assert len(result["chat_history"]) == 2


def test_tavily_fallback_when_docs_missing(mock_services, isolated_checkpoint):
    mock_services["state"]["pinecone_handler"] = lambda query, top_k=5: EMPTY_PINECONE

    result = run_rag("What is the latest Docker release?", "thread-tavily")

    assert mock_services["calls"]["pinecone"]
    assert mock_services["calls"]["tavily"]
    assert len(result["context"]) == 1
    assert result["context"][0]["origin"] == "tavily"
    assert "docker-27" in result["context"][0]["source"]
    assert "Docker 27.0" in result["answer"]


def test_tavily_fallback_when_docs_low_relevance(mock_services, isolated_checkpoint):
    mock_services["state"]["pinecone_handler"] = lambda query, top_k=5: LOW_SCORE_PINECONE

    result = run_rag("What is the latest Docker release?", "thread-low-score")

    assert mock_services["calls"]["tavily"]
    assert result["context"][0]["origin"] == "tavily"


def test_conversation_accumulates_history_same_thread(mock_services, isolated_checkpoint):
    first = run_rag("What is LangGraph?", "thread-convo")
    second = run_rag("Tell me more about that.", "thread-convo")

    assert len(first["chat_history"]) == 2
    assert len(second["chat_history"]) == 4
    assert second["chat_history"][0]["content"] == "What is LangGraph?"
    assert second["chat_history"][1]["role"] == "assistant"
    assert second["chat_history"][2]["content"] == "Tell me more about that."


def test_different_threads_have_isolated_history(mock_services, isolated_checkpoint):
    first = run_rag("What is LangGraph?", "thread-a")
    second = run_rag("What is Docker?", "thread-b")

    assert len(first["chat_history"]) == 2
    assert len(second["chat_history"]) == 2
    assert second["chat_history"][0]["content"] == "What is Docker?"
    assert first["chat_history"][0]["content"] == "What is LangGraph?"
    assert first["chat_history"] != second["chat_history"]


def test_conversation_docs_then_tavily_uses_both_contexts(mock_services, isolated_checkpoint):
    pinecone_calls = {"count": 0}

    def pinecone_switch(query: str, top_k: int = 5) -> dict:
        pinecone_calls["count"] += 1
        if pinecone_calls["count"] == 1:
            return pinecone_with_docs(query, top_k)
        return EMPTY_PINECONE

    mock_services["state"]["pinecone_handler"] = pinecone_switch
    mock_services["state"]["llm_handler"] = make_llm_handler(
        rewrite_map={
            "What is LangGraph?": "LangGraph framework overview",
            "And what about Docker 27?": "Docker 27 release features",
        }
    )

    first = run_rag("What is LangGraph?", "thread-mixed")
    second = run_rag("And what about Docker 27?", "thread-mixed")

    assert first["context"][0]["origin"] == "pinecone"
    assert second["context"][0]["origin"] == "tavily"
    assert len(second["chat_history"]) == 4

    generate_prompts = [
        prompt
        for prompt in mock_services["calls"]["llm"]
        if "Answer the question using the context below." in prompt
    ]
    assert len(generate_prompts) == 2
    assert "langgraph/overview.md" in generate_prompts[0].lower()
    assert "What is LangGraph?" in generate_prompts[1]
    assert "docker 27.0" in generate_prompts[1].lower()
    assert "Earlier we discussed LangGraph" in second["answer"]


def test_rewrite_receives_prior_conversation_on_follow_up(mock_services, isolated_checkpoint):
    mock_services["state"]["llm_handler"] = make_llm_handler(
        rewrite_map={
            "What are its main nodes?": "LangGraph workflow main nodes",
        }
    )

    run_rag("What is LangGraph?", "thread-rewrite")
    run_rag("What are its main nodes?", "thread-rewrite")

    rewrite_prompts = [
        prompt for prompt in mock_services["calls"]["llm"] if "Rewritten query:" in prompt
    ]
    assert len(rewrite_prompts) >= 2
    assert "What is LangGraph?" in rewrite_prompts[1]
    assert "LangGraph is a stateful LLM workflow framework" in rewrite_prompts[1]
