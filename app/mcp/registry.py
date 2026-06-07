from app.mcp import github, tavily, pinecone, langsmith, fastapi, python


MCP_TOOLS = {
    "github": github,
    "tavily": tavily,
    "pinecone": pinecone,
    "langsmith": langsmith,
    "fastapi": fastapi,
    "python": python,
}

def get_tool(name: str):
    return MCP_TOOLS[name]