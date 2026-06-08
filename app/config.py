import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "knowledge-graph-ai")
PINECONE_EMBEDDING_MODEL = os.getenv(
    "PINECONE_EMBEDDING_MODEL", "multilingual-e5-large"
)
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1024"))

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
DATA_DIR = os.getenv("DATA_DIR", "data/docs")
RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))
RELEVANCE_THRESHOLD = float(os.getenv("RELEVANCE_THRESHOLD", "0.75"))

LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_ENDPOINT = os.getenv(
    "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
)
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "knowledge-graph-ai")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
