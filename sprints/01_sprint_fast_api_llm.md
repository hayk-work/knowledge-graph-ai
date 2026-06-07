# Sprint 1 — FastAPI + LLM

## Goal

Expose an API endpoint that generates responses using Groq.

## Tasks

### Create API

Endpoints:

```http
GET /health
POST /ask
```

### Implement LLM Service

Create:

```text
app/llm/
```

Responsibilities:

* initialize Groq
* invoke model
* return response

### Test Endpoint

Request:

```json
{
  "question": "What is FastAPI?"
}
```

Response:

```json
{
  "answer": "..."
}
```

## Definition of Done

* FastAPI running
* Swagger docs available
* LLM responds through API
