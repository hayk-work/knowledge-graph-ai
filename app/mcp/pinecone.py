from pinecone import Pinecone
from app.config import PINECONE_API_KEY, PINECONE_INDEX
from app.retriever.embeddings import embed_text

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)


def run(query: str, top_k: int = 5) -> dict:
    """
    Vector search tool for LangGraph / RAG pipeline
    """

    vector = embed_text(query)

    results = index.query(
        vector=vector,
        top_k=top_k,
        include_metadata=True
    )

    return {
        "query": query,
        "top_k": top_k,
        "matches": [
            {
                "score": match.score,
                "text": match.metadata.get("text"),
                "source": match.metadata.get("source")
            }
            for match in results.matches
        ]
    }
