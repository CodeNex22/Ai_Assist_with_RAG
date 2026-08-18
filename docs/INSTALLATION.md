# Installation Guide

## Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose v2
- 8GB+ RAM recommended for local inference

## Steps

1. Clone the repository and change into it.
2. Copy `.env.example` to `.env`.
3. Start the stack:

```bash
docker compose up --build
```

4. Open the frontend at http://localhost:5173.
5. Upload a document and ask questions about it.

> If you want to use the optional Ollama service profile, start with `docker compose --profile ollama up --build`.
