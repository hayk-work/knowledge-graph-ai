REWRITE_QUERY_PROMPT = """Rewrite the user query into a clear, detailed search query for documentation retrieval.
Expand abbreviations, add relevant technical terms, and keep the original intent.
Keep the rewritten query concise (under 400 characters).
Return only the rewritten query with no explanation.

Conversation context:
{history_or_summary}

Original query: {question}

Rewritten query:"""
