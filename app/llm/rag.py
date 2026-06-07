from app.llm.groq_client import invoke
from app.retriever.pinecone_retriever import RetrievedDocument


def _format_context(documents: list[RetrievedDocument]) -> str:
    if not documents:
        return "No relevant documents found."

    blocks = []
    for doc in documents:
        blocks.append(f"Source: {doc.source}\n{doc.text}")
    return "\n\n---\n\n".join(blocks)


def generate_answer(question: str, documents: list[RetrievedDocument]) -> str:
    context = _format_context(documents)
    prompt = f"""Answer the question using the context below.
Cite the source filename or URL when stating facts.
If the context does not contain enough information, say you do not have enough information.

Context:
{context}

Question: {question}

Answer:"""
    return invoke(prompt)
