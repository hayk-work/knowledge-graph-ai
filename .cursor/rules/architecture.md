# Architecture Rules

This project is a LangGraph-based Agentic RAG system.

Core rule:
All external systems must be accessed through `app/mcp/` tools.

Flow:
User → FastAPI → LangGraph → MCP Tools → LLM → Response

Do not bypass MCP layer in nodes or chains.