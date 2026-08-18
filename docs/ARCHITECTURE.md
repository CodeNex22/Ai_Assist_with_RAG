# Architecture

```mermaid
flowchart LR
    User[User] --> UI[React frontend]
    UI --> API[FastAPI backend]
    API --> RAG[RAG pipeline]
    RAG --> Ollama[Ollama LLM]
    RAG --> Qdrant[Qdrant vector DB]
    API --> Postgres[PostgreSQL]
    API --> Docs[Uploaded documents]
```

The application keeps the chat experience, document ingestion, and retrieval logic behind a service layer so a future WhatsApp, Telegram, or Teams adapter can reuse the same core pipeline.
