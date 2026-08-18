from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    chat_id: str | None = None
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    chat_id: str
    answer: str
    sources: list[str] = Field(default_factory=list)
    used_rag: bool = True


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str


class DocumentSummary(BaseModel):
    id: str
    filename: str
    size: int
    uploaded_at: str


class HealthResponse(BaseModel):
    status: str
    ollama: str
    qdrant: str
    database: str


class ModelResponse(BaseModel):
    models: list[str]
