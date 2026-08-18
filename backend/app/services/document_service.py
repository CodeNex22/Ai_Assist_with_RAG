import uuid
from pathlib import Path
from typing import Any

from docx import Document as DocxDocument
from markdown import markdown as to_markdown_html
from pypdf import PdfReader

from app.core.config import settings
from app.core.logging import get_logger
from app.embeddings.embedding_service import EmbeddingService
from app.rag.chunking import chunk_text
from app.rag.vector_store import VectorStore

logger = get_logger(__name__)


class DocumentService:
    def __init__(self, embedding_service: EmbeddingService, vector_store: VectorStore) -> None:
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def ingest(self, filename: str, content: bytes) -> dict[str, Any]:
        safe_name = Path(filename).name
        file_path = self.upload_dir / safe_name
        file_path.write_bytes(content)

        text = self._extract_text(filename, content)
        chunks = chunk_text(text, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap)

        document_id = str(uuid.uuid4())
        for index, chunk in enumerate(chunks):
            embedding = await self.embedding_service.embed_text(chunk)
            self.vector_store.upsert(
                document_id=document_id,
                chunk_id=f"{document_id}-{index}",
                text=chunk,
                embedding=embedding,
                metadata={"filename": safe_name, "chunk_index": index},
            )

        return {"document_id": document_id, "filename": safe_name, "chunks": len(chunks)}

    def _extract_text(self, filename: str, content: bytes) -> str:
        suffix = Path(filename).suffix.lower()
        if suffix == ".txt":
            return content.decode("utf-8", errors="ignore")
        if suffix == ".md":
            return content.decode("utf-8", errors="ignore")
        if suffix == ".csv":
            return content.decode("utf-8", errors="ignore")
        if suffix == ".pdf":
            reader = PdfReader(file_path := Path(self.upload_dir / Path(filename).name))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        if suffix == ".docx":
            doc = DocxDocument(file_path := Path(self.upload_dir / Path(filename).name))
            return "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
        return content.decode("utf-8", errors="ignore")
