from dataclasses import dataclass

from app.config import RETRIEVAL_TOP_K
from app.mcp import pinecone


@dataclass
class RetrievedDocument:
    text: str
    source: str
    score: float


def retrieve(question: str, top_k: int | None = None) -> list[RetrievedDocument]:
    k = top_k if top_k is not None else RETRIEVAL_TOP_K
    result = pinecone.run(question, top_k=k)

    documents: list[RetrievedDocument] = []
    for match in result["matches"]:
        text = match.get("text")
        if not text:
            continue
        documents.append(
            RetrievedDocument(
                text=text,
                source=match.get("source") or "unknown",
                score=float(match.get("score") or 0.0),
            )
        )

    return documents
