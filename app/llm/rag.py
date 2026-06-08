from app.llm.groq_client import invoke
from app.memory.history import format_history_for_prompt
from app.retriever.pinecone_retriever import RetrievedDocument


def _format_context(documents: list[RetrievedDocument]) -> str:
    if not documents:
        return "No relevant documents found."

    blocks = []
    for doc in documents:
        blocks.append(f"Source: {doc.source}\n{doc.text}")
    return "\n\n---\n\n".join(blocks)


def generate_answer(
    question: str,
    documents: list[RetrievedDocument],
    chat_history: list[dict] | None = None,
    conversation_summary: str = "",
) -> str:
    context = _format_context(documents)
    trimmed_history = format_history_for_prompt(chat_history or [])
    prompt = f"""Answer the question using the context below.
Cite the source filename or URL when stating facts.
If the context does not contain enough information, say you do not have enough information.
If conversation memory conflicts with retrieved context, prefer retrieved context.

Conversation summary:
{conversation_summary or "No summary available."}

Conversation history (recent):
{trimmed_history}

Context:
{context}

Question: {question}

Answer:"""
    return invoke(prompt)
