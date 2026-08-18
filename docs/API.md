# API Reference

## Chat

- POST /chat: Send a chat message and receive a grounded answer.
- GET /chats: Retrieve known chats.
- GET /chat/{chat_id}: Retrieve a specific chat.
- DELETE /chat/{chat_id}: Remove a chat.

## Documents

- POST /documents/upload: Upload a document to the RAG pipeline.
- GET /documents: List available documents.
- DELETE /documents/{document_id}: Delete a document.

## Utility

- GET /health: Basic health check.
- GET /models: List configured models.
- POST /settings/model: Update the active model setting.
