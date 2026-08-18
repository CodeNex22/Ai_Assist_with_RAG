from fastapi import APIRouter

from app.core.config import settings
from app.models.schemas import ModelResponse

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=ModelResponse)
async def list_models() -> ModelResponse:
    return ModelResponse(models=[settings.ollama_model, settings.embedding_model])
