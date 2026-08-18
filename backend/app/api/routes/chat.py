from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import AppContainer, get_container
from app.models.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, container: AppContainer = Depends(get_container)) -> ChatResponse:
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    answer, sources, used_rag, chat_id = await container.chat_service.answer(
        request.message,
        chat_id=request.chat_id,
        history=[message.model_dump() for message in request.history],
    )
    return ChatResponse(chat_id=chat_id, answer=answer, sources=sources, used_rag=used_rag)


@router.get("/chats")
async def list_chats(container: AppContainer = Depends(get_container)) -> list[dict[str, object]]:
    return [{"id": chat.id, "title": chat.title} for chat in container.chat_repository.list()]


@router.get("/chat/{chat_id}")
async def get_chat(chat_id: str, container: AppContainer = Depends(get_container)) -> dict[str, object]:
    chat = container.chat_repository.get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return {"id": chat.id, "title": chat.title, "messages": chat.messages}


@router.delete("/chat/{chat_id}")
async def delete_chat(chat_id: str, container: AppContainer = Depends(get_container)) -> dict[str, str]:
    container.chat_repository.delete(chat_id)
    return {"status": "deleted", "chat_id": chat_id}
