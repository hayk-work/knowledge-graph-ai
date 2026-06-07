# 🧠 KnowledgeGraph AI

**Agentic RAG Documentation Assistant built with LangGraph, LangChain, Pinecone, Groq, and FastAPI.**

KnowledgeGraph AI is a production-style Retrieval-Augmented Generation (RAG) system that answers user questions using trusted documentation sources. The application combines semantic search, query rewriting, graph-based orchestration, and source-grounded answer generation to deliver accurate and explainable responses.

---

## 🚀 Features

* 🔍 Semantic document retrieval with Pinecone
* 🧠 Query rewriting for improved search quality
* 🔗 LangGraph-based workflow orchestration
* 📚 Retrieval-Augmented Generation (RAG)
* 🌐 Tavily fallback web search for missing information
* 📖 Source citations in generated answers
* 📊 LangSmith observability and tracing
* ⚡ Groq-powered low-latency inference
* 🚀 FastAPI REST API

---

## 🏗️ Architecture

```text
User
 │
 ▼
FastAPI
 │
 ▼
LangGraph Workflow
 │
 ├── Rewrite Query
 │
 ├── Retrieve Documents (Pinecone)
 │
 ├── Grade Retrieved Context
 │       │
 │       ├── Relevant → Generate Answer
 │       │
 │       └── Not Relevant
 │               │
 │               ▼
 │        Tavily Web Search
 │               │
 │               ▼
 │        Generate Answer
 │
 ▼
Answer + Citations
 │
 ▼
LangSmith Tracing
```

External systems are accessed through the MCP tool layer in `app/mcp/`.

---

## 🛠️ Tech Stack

| Component             | Technology |
| --------------------- | ---------- |
| API                   | FastAPI    |
| Workflow Engine       | LangGraph  |
| LLM Framework         | LangChain  |
| LLM Provider          | Groq       |
| Vector Database       | Pinecone   |
| Embeddings            | Pinecone Inference |
| Web Search            | Tavily     |
| Observability         | LangSmith  |
| Dependency Management | uv         |

---

## 📁 Project Structure

```text
knowledge-graph-ai/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── graph/
│   │   ├── nodes/
│   │   │   ├── rewrite.py
│   │   │   ├── retrieve.py
│   │   │   ├── grade.py
│   │   │   ├── web_search.py
│   │   │   ├── generate.py
│   │   │   └── routing.py
│   │   ├── workflow.py
│   │   ├── state.py
│   │   └── sources.py
│   │
│   ├── ingestion/
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   └── pipeline.py
│   │
│   ├── mcp/
│   │   ├── pinecone.py
│   │   ├── tavily.py
│   │   └── ...
│   │
│   ├── retriever/
│   │   ├── pinecone_retriever.py
│   │   └── embeddings.py
│   │
│   ├── llm/
│   │   ├── groq_client.py
│   │   └── rag.py
│   │
│   ├── prompts/
│   │
│   └── config.py
│
├── data/docs/          # Source documents (operator-side)
├── scripts/
│   └── seed_pinecone.py
│
├── sprints/
├── .env
├── pyproject.toml
├── README.md
└── main.py
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root (see `.env.example`).

```env
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant

PINECONE_API_KEY=
PINECONE_INDEX=knowledge-graph-ai
PINECONE_EMBEDDING_MODEL=multilingual-e5-large
EMBEDDING_DIMENSION=1024

TAVILY_API_KEY=

CHUNK_SIZE=1000
CHUNK_OVERLAP=200
DATA_DIR=data/docs
RETRIEVAL_TOP_K=5
RELEVANCE_THRESHOLD=0.75

LANGCHAIN_TRACING_V2=true
LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=knowledge-graph-ai
```

---

## 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/knowledge-graph-ai.git
cd knowledge-graph-ai
```

### Create Virtual Environment

```bash
uv venv
source .venv/bin/activate   # Linux / macOS
```

### Install Dependencies

```bash
uv sync
```

### Configure Environment

```bash
cp .env.example .env
```

Required keys:

* `GROQ_API_KEY` — LLM inference
* `PINECONE_API_KEY` — vector search and embeddings
* `TAVILY_API_KEY` — web search fallback

### Seed the Knowledge Base

Documents must be indexed in Pinecone **before** users can ask questions. Sample docs live under `data/docs/` (LangChain, LangGraph, RAG, Kubernetes, Docker, FastAPI).

Run once after install (and again when docs change):

```bash
uv run python scripts/seed_pinecone.py
```

This loads `.md` / `.txt` files, chunks them, embeds via Pinecone Inference, and upserts into `PINECONE_INDEX`.

---

## ▶️ Running the Application

```bash
uv run uvicorn main:app --reload
```

* API: http://localhost:8000
* Swagger docs: http://localhost:8000/docs

---

## 📡 API

### `GET /health`

Health check.

### `POST /ingest` (operator)

Index documents from `data/docs/`.

```json
{ "path": "" }
```

### `POST /ask`

```json
{
  "question": "What is LangGraph?"
}
```

Response:

```json
{
  "answer": "LangGraph is a library for building stateful, multi-step AI workflows...",
  "sources": [
    "pinecone:langgraph/overview.md",
    "pinecone:langchain/overview.md"
  ],
  "context": [
    {
      "text": "...",
      "source": "langgraph/overview.md",
      "score": 0.88,
      "origin": "pinecone"
    }
  ]
}
```

When Pinecone has no relevant match, the graph falls back to Tavily. Sources are prefixed with `tavily:` and `origin` is `"tavily"`.

---

## 🔄 LangGraph Workflow

```text
START → rewrite → retrieve → grade
                              ├─ relevant  → generate → END
                              └─ irrelevant → web_search → generate → END
```

| Node       | Responsibility                           |
| ---------- | ---------------------------------------- |
| Rewrite    | Expand short/vague queries for retrieval |
| Retrieve   | Semantic search in Pinecone              |
| Grade      | Score relevance; route next step         |
| Web Search | Tavily fallback when docs are insufficient |
| Generate   | Groq answer grounded on context          |

---

## 📊 Observability

Set `LANGCHAIN_TRACING_V2=true` and `LANGSMITH_API_KEY` in `.env`. Each `/ask` request traces the full graph in LangSmith with node timing, prompts, and outputs.

View traces at your [LangSmith dashboard](https://smith.langchain.com/).

---

## 🎯 Learning Goals

This project demonstrates:

* Retrieval-Augmented Generation (RAG)
* Agentic workflows with LangGraph
* Semantic search using Pinecone
* Query rewriting and document grading
* Conditional graph routing with Tavily fallback
* Production API design
* LLM observability with LangSmith

---

## 🛣️ Future Improvements

* Conversation memory
* Hybrid retrieval
* Multi-query retrieval
* Answer evaluation node
* Streaming responses
* React / Next.js frontend
* Authentication and rate limiting

---

## 📜 License

MIT License

---

Built to explore modern AI application architecture with LangGraph, LangChain, Pinecone, Groq, and FastAPI.
