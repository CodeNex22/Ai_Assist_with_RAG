from app.core.config import settings
from app.core.logging import get_logger
from app.services.ollama_service import OllamaService

logger = get_logger(__name__)


class EmbeddingService:
    def __init__(self, ollama_service: OllamaService | None = None) -> None:
        self.ollama_service = ollama_service or OllamaService()

    async def embed_text(self, text: str) -> list[float]:
        return await self.ollama_service.embed(text, model=settings.embedding_model)
