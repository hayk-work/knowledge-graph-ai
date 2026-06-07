# Retrieval-Augmented Generation (RAG)

RAG combines information retrieval with text generation. Instead of relying only on what an
LLM memorized during training, the system fetches relevant documents at query time and
conditions the answer on that context.

## The Problem RAG Solves

LLMs can hallucinate facts, lack knowledge of private data, and have stale training cutoffs.
RAG grounds responses in a curated knowledge base you control.

## RAG Pipeline Stages

### 1. Ingestion (offline)

Documents are loaded, split into chunks, embedded, and stored in a vector database such as
Pinecone. Metadata (source file, section, timestamps) travels with each chunk.

### 2. Retrieval (online)

When a user asks a question, the query is embedded and compared to stored vectors via
semantic similarity. Top-k chunks become the retrieval context.

### 3. Generation

The LLM receives the user question plus retrieved chunks in its prompt. It synthesizes an
answer grounded in those sources and can cite where information came from.

## Chunking Strategy

Text splitters (e.g. `RecursiveCharacterTextSplitter`) break documents into overlapping
segments. Typical settings: 500–1500 characters per chunk with 10–20% overlap. Good chunking
balances context size with retrieval precision.

## Embedding Models

Embeddings map text to dense vectors. Query and document embeddings must come from the same
model. Similar meaning yields vectors that are close in cosine distance.

## Vector Search

Vector databases index embeddings for fast approximate nearest neighbor search. Results
include similarity scores; low scores may trigger fallbacks like web search or “I don’t know.”

## Agentic RAG

Advanced systems add query rewriting, document grading, re-ranking, and tool use. LangGraph
orchestrates these steps with conditional routing—for example, Tavily web search when
Pinecone returns no relevant match.

## Evaluation

Measure RAG quality with retrieval metrics (recall@k, MRR) and generation metrics (faithfulness,
answer relevance). LangSmith helps trace each step for debugging and improvement.
