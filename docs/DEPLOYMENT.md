# Deployment Guide

The project is Docker-first and is intended to run locally with a single command:

```bash
docker compose up --build
```

For production-like deployments, expose the backend and frontend through a reverse proxy and keep the Ollama and Qdrant services on private networking. Use environment variables for model selection and storage paths.
