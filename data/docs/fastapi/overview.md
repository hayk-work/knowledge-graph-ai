# FastAPI Overview

FastAPI is a modern Python web framework for building APIs. It is designed for speed,
developer productivity, and automatic OpenAPI documentation generation.

## Key Features

- High performance, comparable to NodeJS and Go
- Automatic interactive API docs at `/docs`
- Type hints and Pydantic validation
- Async support out of the box
- Built on Starlette and Pydantic

## Basic Example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

## When to Use FastAPI

FastAPI works well for REST APIs, microservices, and backend services that need
strong typing, validation, and low-latency request handling.
