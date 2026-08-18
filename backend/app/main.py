from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import chat, documents, health, models, settings

app = FastAPI(title="AI Customer Support Assistant", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(documents.router)
app.include_router(health.router)
app.include_router(models.router)
app.include_router(settings.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "AI Customer Support Assistant API"}
