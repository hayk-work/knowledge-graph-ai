from openai import OpenAI
from app.config import EMBEDDING_MODEL

client = OpenAI()

def embed_text(text: str):
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding