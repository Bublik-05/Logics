"""
Single endpoint: upload a document, get back how many chunks it was split into.
No listing, no status polling, no versions — just enough to prove ingestion works.
"""
from fastapi import APIRouter, UploadFile

from app.schemas.document import DocumentUploadResponse
from app.services.document_service import process_document

router = APIRouter()


@router.post("/", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile) -> DocumentUploadResponse:
    result = await process_document(file)
    return DocumentUploadResponse(**result)
