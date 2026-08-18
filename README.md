# AI Customer Support Assistant

A local-first AI customer support assistant built with FastAPI, React, Ollama, Qdrant, and PostgreSQL. The application is designed to run entirely on a local machine and can later be extended with WhatsApp Business Cloud API or other messaging adapters without changing the core RAG pipeline.

## Features

- Local chat interface with dark mode and responsive layout
- RAG pipeline using Ollama and Qdrant
- Document upload for PDF, DOCX, TXT, Markdown, and CSV
- Conversation memory and modular services
- Docker Compose setup for local development

## Quick start

1. Copy .env.example to .env
2. Start the stack with Docker Compose
3. Open http://localhost:5173

```bash
docker compose up --build
```

## Project structure

- backend: FastAPI services, routes, and RAG pipeline
- frontend: React + TypeScript + Vite UI
- documents: sample documents ready for indexing
- docker: container build files
