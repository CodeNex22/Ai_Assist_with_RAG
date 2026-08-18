from app.chat.service import ChatService
from app.embeddings.embedding_service import EmbeddingService
from app.rag.vector_store import VectorStore
from app.repositories.chat_repository import ChatRepository
from app.services.document_service import DocumentService
from app.services.ollama_service import OllamaService


class AppContainer:
    def __init__(self) -> None:
        self._ollama_service: OllamaService | None = None
        self._embedding_service: EmbeddingService | None = None
        self._vector_store: VectorStore | None = None
        self._chat_repository: ChatRepository | None = None
        self._chat_service: ChatService | None = None
        self._document_service: DocumentService | None = None

    @property
    def ollama_service(self) -> OllamaService:
        if self._ollama_service is None:
            self._ollama_service = OllamaService()
        return self._ollama_service

    @property
    def embedding_service(self) -> EmbeddingService:
        if self._embedding_service is None:
            self._embedding_service = EmbeddingService(self.ollama_service)
        return self._embedding_service

    @property
    def vector_store(self) -> VectorStore:
        if self._vector_store is None:
            self._vector_store = VectorStore()
        return self._vector_store

    @property
    def chat_repository(self) -> ChatRepository:
        if self._chat_repository is None:
            self._chat_repository = ChatRepository()
        return self._chat_repository

    @property
    def chat_service(self) -> ChatService:
        if self._chat_service is None:
            self._chat_service = ChatService(
                ollama_service=self.ollama_service,
                embedding_service=self.embedding_service,
                vector_store=self.vector_store,
                repository=self.chat_repository,
            )
        return self._chat_service

    @property
    def document_service(self) -> DocumentService:
        if self._document_service is None:
            self._document_service = DocumentService(self.embedding_service, self.vector_store)
        return self._document_service


_container = AppContainer()


def get_container() -> AppContainer:
    return _container
