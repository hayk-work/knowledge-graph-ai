# KnowledgeGraph AI

Agentic RAG assistant built with **LangGraph**, **Pinecone**, **Groq**, and **FastAPI**.

Answers questions using a pre-indexed knowledge base. If Pinecone has no good match, it falls back to **Tavily** web search.

Multi-turn conversations are supported via `thread_id`. Memory is checkpointed in SQLite, trimmed for prompts, and summarized for long sessions.

```text
POST /ask { question, thread_id? }
    ↓
summarize → rewrite → Pinecone retrieve → grade → generate
    ↑              └─ (if bad) → Tavily → generate
memory (trim + summary, checkpointed per thread_id)
```

Retrieval still runs every turn — memory does not bypass Pinecone or Tavily.

---

## Conversation memory

| Layer | What it does |
| ----- | ------------ |
| **Checkpoint** | Persists graph state per `thread_id` in `data/checkpoints.db` |
| **Trim** | Sends only the last N turns to the LLM (default: 6 messages) |
| **Summary** | Compresses older turns when history exceeds the threshold (default: 10 messages) |
| **Rewrite** | Resolves vague follow-ups using recent history and summary |

Pass `thread_id` from a previous response to continue a chat. Omit it for a one-off question.

---

## Setup

```bash
git clone https://github.com/hayk-work/knowledge-graph-ai.git
cd knowledge-graph-ai

uv venv && source .venv/bin/activate
uv sync

cp .env.example .env   # add GROQ_API_KEY, PINECONE_API_KEY, TAVILY_API_KEY

# optional — LangSmith tracing
# LANGCHAIN_TRACING_V2=true
# LANGCHAIN_API_KEY=
# LANGCHAIN_PROJECT=knowledge-graph-ai
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

Response includes `answer`, `sources`, retrieved `context`, and `thread_id`.

## Multi-turn conversations

Use the returned `thread_id` to continue the same conversation:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are its main nodes?", "thread_id": "YOUR_THREAD_ID"}'
```

If you omit `thread_id`, the API creates a new one for a one-off turn.

To clear a conversation session:

```bash
curl -X DELETE http://localhost:8000/threads/YOUR_THREAD_ID
```

---

## API

| Endpoint | Description |
| -------- | ----------- |
| `GET /health` | Health check |
| `POST /ask` | Ask a question |
| `DELETE /threads/{thread_id}` | Clear conversation checkpoint |
| `POST /ingest` | Re-index docs from `data/docs/` (operator) |

`DELETE /threads/{thread_id}` returns `{ "deleted": true, "thread_id": "..." }`.

---

## Tests

```bash
uv run pytest
```

The suite covers single-turn docs retrieval, Tavily fallback, conversation history, thread isolation, checkpoint persistence, and query-length safety for Tavily.

---

MIT License
