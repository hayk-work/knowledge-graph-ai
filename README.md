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

---

## 🛠️ Tech Stack

| Component             | Technology |
| --------------------- | ---------- |
| API                   | FastAPI    |
| Workflow Engine       | LangGraph  |
| LLM Framework         | LangChain  |
| LLM Provider          | Groq       |
| Vector Database       | Pinecone   |
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
│   │   ├── workflow.py
│   │   ├── nodes.py
│   │   └── state.py
│   │
│   ├── retriever/
│   │   ├── pinecone.py
│   │   └── embeddings.py
│   │
│   ├── llm/
│   │   └── groq_client.py
│   │
│   ├── prompts/
│   │
│   └── config.py
│
├── tests/
│
├── .env
├── pyproject.toml
├── README.md
└── main.py
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=
GROQ_MODEL=llama-3.1-8b-instant

PINECONE_API_KEY=
PINECONE_INDEX=knowledge-graph-ai

TAVILY_API_KEY=

EMBEDDING_MODEL=text-embedding-3-small

LANGCHAIN_TRACING_V2=true
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
```

### Activate Environment

Linux / macOS

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

### Install Dependencies

```bash
uv sync
```

Or manually:

```bash
uv add fastapi uvicorn langchain langgraph pinecone python-dotenv langsmith langchain-groq tavily-python
```

---

## ▶️ Running the Application

```bash
uv run uvicorn main:app --reload
```

API available at:

```text
http://localhost:8000
```

Interactive API docs:

```text
http://localhost:8000/docs
```

---

## 📡 API Example

### Request

```http
POST /ask
```

```json
{
  "question": "How does FastAPI dependency injection work?"
}
```

### Response

```json
{
  "answer": "FastAPI uses dependency injection through the Depends function...",
  "sources": [
    "fastapi_docs_dependency_injection",
    "fastapi_tutorial_dependencies"
  ]
}
```

---

## 🔄 LangGraph Workflow

The workflow is implemented as a directed graph where each node performs a specific task.

### Nodes

| Node       | Responsibility                           |
| ---------- | ---------------------------------------- |
| Rewrite    | Improve user query                       |
| Retrieve   | Search Pinecone                          |
| Grade      | Evaluate document relevance              |
| Web Search | Search Tavily if context is insufficient |
| Generate   | Produce grounded answer                  |

### Benefits

* Modular architecture
* Easy node replacement
* Conditional routing
* Scalable agent workflows
* Improved observability

---

## 📊 Observability

KnowledgeGraph AI integrates with LangSmith to provide:

* Graph execution traces
* Node-level timing
* Prompt inspection
* Input/output analysis
* Debugging and evaluation

---

## 🎯 Learning Goals

This project demonstrates:

* Retrieval-Augmented Generation (RAG)
* Agentic workflows with LangGraph
* Semantic search using Pinecone
* Query rewriting strategies
* Conditional graph routing
* Production API design
* LLM observability with LangSmith

---

## 🛣️ Future Improvements

* Conversation memory
* Hybrid retrieval
* Multi-query retrieval
* Answer evaluation node
* Streaming responses
* Multi-agent architecture
* React / Next.js frontend
* Authentication and rate limiting

---

## 📜 License

MIT License

---

Built to explore modern AI application architecture with LangGraph, LangChain, Pinecone, Groq, and FastAPI.
