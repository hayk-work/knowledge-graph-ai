from tavily import TavilyClient

from app.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)


def web_search(query: str):
    return client.search(query)