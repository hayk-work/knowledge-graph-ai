# Sprint 3 — RAG Retrieval

## Goal
Connect Pinecone retrieval to user queries.

---

## Tasks

### 1. Build retriever module
Create:
app/retriever/pinecone_retriever.py

Responsibilities:
- embed query
- search Pinecone
- return top-k chunks

---

### 2. Define retrieval function

Input:
- user question

Output:
- relevant documents
- metadata (source, score)

---

### 3. Integrate with API

Flow:

User Question → Retriever → Return Context

---

## Done when

- Pinecone returns relevant docs
- API includes retrieved context