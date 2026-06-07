# MCP Tooling Rules

This project uses a local MCP-style tool layer located in `app/mcp/`.

## Available tools:

- github_tool → GitHub repository access
- tavily_tool → web search fallback
- pinecone_tool → vector database retrieval
- langsmith_tool → tracing and observability
- fastapi_tool → API testing client
- python_tool → code execution

## Rules:

- NEVER call external APIs directly in LangGraph nodes
- ALWAYS use MCP tools instead
- Use pinecone_tool for retrieval first
- Use tavily_tool only when retrieval fails
- Log important steps using langsmith_tool