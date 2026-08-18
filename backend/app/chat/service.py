import uuid
from typing import Any

from app.core.config import settings
from app.core.logging import get_logger
from app.embeddings.embedding_service import EmbeddingService
from app.rag.chunking import chunk_text
from app.rag.vector_store import VectorStore
from app.repositories.chat_repository import ChatRepository
from app.services.ollama_service import OllamaService

logger = get_logger(__name__)


class ChatService:
    def __init__(
        self,
        ollama_service: OllamaService,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        repository: ChatRepository,
    ) -> None:
        self.ollama_service = ollama_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.repository = repository

    async def answer(self, message: str, chat_id: str | None = None, history: list[dict[str, Any]] | None = None) -> tuple[str, list[str], bool, str]:
        chat_id = chat_id or str(uuid.uuid4())
        history = history or []
        self.repository.create(chat_id, "Support chat")
        self.repository.append_message(chat_id, {"role": "user", "content": message})

        if not self.vector_store.points:
            self.repository.append_message(chat_id, {"role": "assistant", "content": "I couldn't find that information in the uploaded documents."})
            return "I couldn't find that information in the uploaded documents.", [], False, chat_id

        embedding = await self.embedding_service.embed_text(message)
        candidates = self.vector_store.search(embedding, top_k=settings.top_k)
        context = "\n\n".join(item["text"] for item in candidates if item.get("text"))

        prompt = (
            "You are a helpful customer support assistant. Answer only using the provided context. "
            "If the answer is not present, say exactly: 'I couldn't find that information in the uploaded documents.'\n\n"
            f"Context:\n{context}\n\nQuestion:\n{message}"
        )
        answer = await self.ollama_service.generate(prompt)

        self.repository.append_message(chat_id, {"role": "assistant", "content": answer})
        sources = [item.get("metadata", {}).get("filename", "uploaded-document") for item in candidates]
        return answer, sources, True, chat_id
