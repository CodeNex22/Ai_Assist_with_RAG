from typing import Any

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class VectorStore:
    def __init__(self) -> None:
        self.points: dict[str, dict[str, Any]] = {}

    def upsert(self, document_id: str, chunk_id: str, text: str, embedding: list[float], metadata: dict[str, Any] | None = None) -> None:
        self.points[chunk_id] = {
            "document_id": document_id,
            "text": text,
            "embedding": embedding,
            "metadata": metadata or {},
        }

    def search(self, embedding: list[float], top_k: int = 4) -> list[dict[str, Any]]:
        if not self.points:
            return []
        scored = []
        for chunk_id, point in self.points.items():
            similarity = self._cosine_similarity(embedding, point["embedding"])
            scored.append((similarity, point | {"id": chunk_id}))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in scored[:top_k]]

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float]) -> float:
        if not left or not right:
            return 0.0
        dot = sum(a * b for a, b in zip(left, right))
        norm_left = sum(a * a for a in left) ** 0.5
        norm_right = sum(b * b for b in right) ** 0.5
        if not norm_left or not norm_right:
            return 0.0
        return dot / (norm_left * norm_right)
