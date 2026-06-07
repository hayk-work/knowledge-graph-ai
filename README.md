# KnowledgeGraph AI

Agentic RAG assistant built with **LangGraph**, **Pinecone**, **Groq**, and **FastAPI**.

Answers questions using a pre-indexed knowledge base. If Pinecone has no good match, it falls back to **Tavily** web search.

```text
question → rewrite → Pinecone retrieve → grade → generate
                                      └─ (if bad) → Tavily → generate
```

---

## Setup

```bash
git clone https://github.com/hayk-work/knowledge-graph-ai.git
cd knowledge-graph-ai

uv venv && source .venv/bin/activate
uv sync

cp .env.example .env   # add GROQ_API_KEY, PINECONE_API_KEY, TAVILY_API_KEY
```

## Index documents (run once)

```bash
uv run python scripts/seed_pinecone.py
```

Sample docs are in `data/docs/`. Add your own `.md` / `.txt` files there and run again.

## Run

```bash
uv run uvicorn main:app --reload
```

Open http://localhost:8000/docs

## Ask a question

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is LangGraph?"}'
```

Response includes `answer`, `sources`, and retrieved `context`.

---

## API

| Endpoint | Description |
| -------- | ----------- |
| `GET /health` | Health check |
| `POST /ask` | Ask a question |
| `POST /ingest` | Re-index docs from `data/docs/` (operator) |

---

MIT License
