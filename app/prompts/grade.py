GRADE_CONTEXT_PROMPT = """You are a grader assessing whether retrieved documents can answer the user question.

Question: {question}

Retrieved documents:
{documents}

Respond with JSON only:
{{"score": <float 0-1>, "decision": "relevant" or "irrelevant"}}

Use "relevant" only if the documents contain enough information to answer the question."""
