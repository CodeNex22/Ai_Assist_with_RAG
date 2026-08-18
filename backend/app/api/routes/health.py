from fastapi import APIRouter

from app.models.schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        ollama="available",
        qdrant="ready",
        database="postgres-ready",
    )
