REWRITE_QUERY_PROMPT = """Rewrite the user query into a clear, detailed search query for documentation retrieval.
Expand abbreviations, add relevant technical terms, and keep the original intent.
Return only the rewritten query with no explanation.

Original query: {question}

Rewritten query:"""
