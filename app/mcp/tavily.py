from tavily import TavilyClient

from app.config import TAVILY_API_KEY, RETRIEVAL_TOP_K

_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    global _client
    if _client is None:
        _client = TavilyClient(api_key=TAVILY_API_KEY)
    return _client


def web_search(query: str, max_results: int | None = None) -> dict:
    limit = max_results if max_results is not None else RETRIEVAL_TOP_K
    return _get_client().search(query=query, max_results=limit)
