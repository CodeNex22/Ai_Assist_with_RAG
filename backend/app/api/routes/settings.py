from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(prefix="/settings", tags=["settings"])


@router.post("/model")
async def update_model(model: str) -> dict[str, str]:
    return {"status": "updated", "model": model}
