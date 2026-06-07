from pinecone import Pinecone

from app.config import PINECONE_API_KEY, PINECONE_EMBEDDING_MODEL

_pc: Pinecone | None = None

EMBED_BATCH_SIZE = 96


def _get_client() -> Pinecone:
    global _pc
    if _pc is None:
        _pc = Pinecone(api_key=PINECONE_API_KEY)
    return _pc


def _embed(inputs: list[str], input_type: str) -> list[list[float]]:
    result = _get_client().inference.embed(
        model=PINECONE_EMBEDDING_MODEL,
        inputs=inputs,
        parameters={"input_type": input_type, "truncate": "END"},
    )
    return [item.values for item in result.data]


def embed_text(text: str) -> list[float]:
    return _embed([text], input_type="query")[0]


def embed_passages(texts: list[str]) -> list[list[float]]:
    embeddings: list[list[float]] = []
    for start in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[start : start + EMBED_BATCH_SIZE]
        embeddings.extend(_embed(batch, input_type="passage"))
    return embeddings
