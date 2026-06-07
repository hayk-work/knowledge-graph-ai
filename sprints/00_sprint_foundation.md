# Sprint 0 — Foundation

## Goal

Fix broken scaffolding so every later sprint starts from a working baseline.

---

## Tasks

### 1. Complete configuration

Update `app/config.py` with all environment variables:

* `GROQ_API_KEY`, `GROQ_MODEL`
* `PINECONE_API_KEY`, `PINECONE_INDEX`, `PINECONE_EMBEDDING_MODEL`
* `TAVILY_API_KEY`
* `LANGCHAIN_TRACING_V2`, `LANGSMITH_API_KEY`, `LANGSMITH_ENDPOINT`, `LANGSMITH_PROJECT`
* `GITHUB_TOKEN`

---

### 2. Fix dependencies

In `pyproject.toml`:

* Remove `pinecone-client` (conflicts with `pinecone`)

Run:

```bash
uv sync
```

---

### 3. Fix environment template

* Rename `.env.exmaple` → `.env.example`

---

### 4. Smoke-test integrations

Verify each module imports without error:

```bash
uv run python -c "from app.config import GROQ_MODEL"
uv run python -c "from app.retriever.embeddings import embed_text"
uv run python -c "from app.mcp.pinecone import run"
```

Optional — test live services if API keys are configured:

* Groq LLM responds
* Pinecone inference returns an embedding vector
* Pinecone index is reachable
* Tavily search works

---

## Architecture note

External systems are accessed through `app/mcp/` tools.
Later sprints build capabilities; MCP remains the integration layer.

Flow:

```text
User → FastAPI → LangGraph → MCP Tools → LLM → Response
```

---

## Done when

* All config imports resolve
* Pinecone package imports without conflict
* `.env.example` matches `app/config.py`
* Project is ready for Sprint 1
