# Docker Overview

Docker packages applications and their dependencies into containers—lightweight, isolated
processes that run consistently on any machine with Docker installed.

## Containers vs Virtual Machines

VMs virtualize hardware and run full operating systems. Containers share the host OS kernel
and isolate processes with namespaces and cgroups. Containers start faster and use less
overhead than VMs.

## Core Concepts

### Image

A read-only template with filesystem layers, runtime, libraries, and app code. Images are
built from a Dockerfile and stored in registries (Docker Hub, ECR, GCR).

### Container

A running instance of an image. Containers are ephemeral; persistent data uses volumes or
bind mounts.

### Dockerfile

Instructions to build an image:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen
COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build: `docker build -t knowledge-graph-ai .`  
Run: `docker run -p 8000:8000 --env-file .env knowledge-graph-ai`

### Volume

Named or bind-mounted storage that survives container restarts. Use volumes for databases
and uploaded files; avoid storing state inside container layers.

### Network

Docker networks let containers communicate by service name. `docker compose` creates a default
network for all services in the stack.

## Docker Compose

Compose defines multi-container apps in `docker-compose.yml`:

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
```

Start: `docker compose up -d`

## Best Practices

- Use slim base images to reduce attack surface and size
- Run as non-root users in production
- Multi-stage builds separate build tools from runtime
- Pin image digests or version tags for reproducibility
- Do not commit secrets; use env files or secret managers

## Docker and Kubernetes

Docker builds the images; Kubernetes orchestrates them at scale. CI pipelines typically
build and push images, then update Kubernetes Deployments to roll out new versions.

## Local Development

Developers run APIs, databases, and workers locally with Compose before deploying the same
container images to staging or production clusters.
