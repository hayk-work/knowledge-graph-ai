from app.mcp import tavily as tavily_module
from app.search.query import clamp_search_query


def test_clamp_search_query_under_limit():
    query = "What is LangGraph?"
    assert clamp_search_query(query, 400) == query


def test_clamp_search_query_truncates_at_word_boundary():
    query = "word " * 120
    result = clamp_search_query(query, 400)

    assert len(result) <= 400
    assert not result.endswith(" ")


def test_tavily_web_search_clamps_before_api(monkeypatch):
    captured: list[str] = []

    class FakeClient:
        def search(self, query: str, max_results: int) -> dict:
            captured.append(query)
            return {"results": []}

    monkeypatch.setattr(tavily_module, "_client", FakeClient())

    tavily_module.web_search("x" * 500)

    assert len(captured) == 1
    assert len(captured[0]) <= 400
