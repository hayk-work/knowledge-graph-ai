from tavily import TavilyClient

from app.config import RETRIEVAL_TOP_K, TAVILY_API_KEY, TAVILY_MAX_QUERY_LENGTH
from app.search.query import clamp_search_query

_client: TavilyClient | None = None


def _get_client() -> TavilyClient:
    global _client
    if _client is None:
        _client = TavilyClient(api_key=TAVILY_API_KEY)
    return _client


def web_search(query: str, max_results: int | None = None) -> dict:
    limit = max_results if max_results is not None else RETRIEVAL_TOP_K
    safe_query = clamp_search_query(query, TAVILY_MAX_QUERY_LENGTH)
    return _get_client().search(query=safe_query, max_results=limit)
