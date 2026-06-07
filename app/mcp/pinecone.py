import hashlib
from typing import Any

from pinecone import Pinecone, ServerlessSpec

from app.config import (
    EMBEDDING_DIMENSION,
    PINECONE_API_KEY,
    PINECONE_INDEX,
)
from app.retriever.embeddings import embed_passages, embed_text

_pc: Pinecone | None = None
_index = None

UPSERT_BATCH_SIZE = 100


def _get_client() -> Pinecone:
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
    return _pc


def _get_index():
    global _index
    if _index is None:
        _index = _get_client().Index(PINECONE_INDEX)
    return _index


def ensure_index() -> str:
    client = _get_client()
    if not client.has_index(PINECONE_INDEX):
        client.create_index(
            name=PINECONE_INDEX,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return PINECONE_INDEX


def _chunk_id(source: str, chunk_index: int) -> str:
    digest = hashlib.sha256(f"{source}:{chunk_index}".encode()).hexdigest()
    return digest[:32]


def upsert_chunks(source: str, chunks: list[str]) -> int:
    if not chunks:
        return 0

    ensure_index()
    index = _get_index()
    vectors = embed_passages(chunks)

    records: list[dict[str, Any]] = []
    for chunk_index, (text, values) in enumerate(zip(chunks, vectors)):
        records.append(
            {
                "id": _chunk_id(source, chunk_index),
                "values": values,
                "metadata": {
                    "text": text,
                    "source": source,
                    "chunk_index": chunk_index,
                },
            }
        )

    for start in range(0, len(records), UPSERT_BATCH_SIZE):
        index.upsert(vectors=records[start : start + UPSERT_BATCH_SIZE])

    return len(records)


def run(query: str, top_k: int = 5) -> dict:
    """
    Vector search tool for LangGraph / RAG pipeline
    """
    vector = embed_text(query)

    results = _get_index().query(
        vector=vector,
        top_k=top_k,
        include_metadata=True,
    )

    return {
        "query": query,
        "top_k": top_k,
        "matches": [
            {
                "score": match.score,
                "text": match.metadata.get("text"),
                "source": match.metadata.get("source"),
            }
            for match in results.matches
        ],
    }
