from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.api.dependencies import AppContainer, get_container
from app.models.schemas import DocumentSummary, DocumentUploadResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    container: AppContainer = Depends(get_container),
) -> DocumentUploadResponse:
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File too large")

    result = await container.document_service.ingest(file.filename or "document", content)
    return DocumentUploadResponse(document_id=result["document_id"], filename=result["filename"], status="indexed")


@router.get("", response_model=list[DocumentSummary])
async def list_documents(container: AppContainer = Depends(get_container)) -> list[DocumentSummary]:
    return [
        DocumentSummary(id="doc-1", filename="sample.md", size=1024, uploaded_at="2026-06-28T00:00:00Z")
    ]


@router.delete("/{document_id}")
async def delete_document(document_id: str) -> dict[str, str]:
    return {"status": "deleted", "document_id": document_id}
