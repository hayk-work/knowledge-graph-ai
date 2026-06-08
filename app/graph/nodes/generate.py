from app.graph.state import State
from app.llm.rag import generate_answer
from app.retriever.pinecone_retriever import RetrievedDocument


def generate_node(state: State) -> dict:
    documents = [
        RetrievedDocument(text=doc["text"], source=doc["source"], score=doc["score"])
        for doc in state["context"]
    ]
    answer = generate_answer(
        state["question"],
        documents,
        chat_history=state.get("chat_history", []),
        conversation_summary=state.get("conversation_summary", ""),
    )
    return {"answer": answer}
