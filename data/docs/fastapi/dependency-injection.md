# FastAPI Dependency Injection

FastAPI has a powerful dependency injection system that helps you manage shared logic,
database connections, authentication, and configuration across your application.

## Depends()

Use `Depends()` to declare dependencies in path operation functions. FastAPI resolves
them automatically before your endpoint runs.

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons
```

## Benefits

- Reusable logic across multiple endpoints
- Easier testing through dependency overrides
- Clear separation between route handlers and shared services
- Automatic validation through Pydantic models used as dependencies

## Common Use Cases

- Database sessions
- Current user authentication
- Pagination parameters
- Shared configuration objects
