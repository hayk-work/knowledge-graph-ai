# LangChain Overview

LangChain is a framework for building applications powered by large language models (LLMs).
It provides abstractions for prompts, models, retrievers, tools, and agents so you can compose
complex AI workflows without reinventing plumbing on every project.

## Core Concepts

### Models

LangChain wraps LLM providers (OpenAI, Groq, Anthropic, and others) behind a common interface.
You invoke a model with messages or a prompt string and receive structured output.

### Prompts

Prompt templates let you parameterize instructions. Instead of hardcoding user input into a
string, you define placeholders and fill them at runtime. This keeps prompts maintainable
and testable.

### Chains

A chain connects steps in sequence: format a prompt, call a model, parse the response.
Early LangChain apps were built mostly from chains before agents and graphs became common.

### Retrievers

Retrievers fetch relevant documents from a vector store or other source. They are the
retrieval half of Retrieval-Augmented Generation (RAG). LangChain retrievers return
`Document` objects with page content and metadata.

### Tools and Agents

Tools are functions an LLM can call (search, calculator, database lookup). Agents decide
which tool to use based on the user question. LangChain standardizes tool schemas and
execution loops.

## LangChain Expression Language (LCEL)

LCEL uses the pipe operator to compose runnable components:

```python
chain = prompt | model | output_parser
result = chain.invoke({"question": "What is RAG?"})
```

Benefits include streaming, batching, parallel execution, and LangSmith tracing out of the box.

## Integrations

LangChain integrates with vector databases (Pinecone, Chroma, FAISS), document loaders,
embedding providers, and observability tools like LangSmith. Most integrations live in
companion packages (`langchain-community`, `langchain-pinecone`, etc.).

## When to Use LangChain

Use LangChain when you need reusable components for RAG, tool calling, or multi-step LLM
workflows. For graph-based orchestration with explicit state and branching, teams often
combine LangChain with LangGraph.
