"""
Document upload — processed synchronously, inline in the request.

This is the one deliberate architectural regression from v2: no Job Queue,
no background worker. For a single-user MVP a multi-second upload response
is acceptable; reintroduce Celery only once this becomes a real problem
(large files, concurrent users), not before.
"""
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config import get_settings
from app.ingestion.chunker import chunk_text
from app.ingestion.parser import extract_text
from app.llm.ollama_client import embed
from app.vectorstore.chroma_client import add_chunks

settings = get_settings()


async def process_document(file: UploadFile) -> dict:
    document_id = str(uuid.uuid4())

    storage_dir = Path(settings.STORAGE_PATH)
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / f"{document_id}_{file.filename}"

    content = await file.read()
    file_path.write_bytes(content)

    text = extract_text(str(file_path), file.content_type or "")
    chunks = chunk_text(text, settings.CHUNK_SIZE_WORDS, settings.CHUNK_OVERLAP_WORDS)

    if not chunks:
        return {"document_id": document_id, "filename": file.filename, "chunk_count": 0}

    embeddings = [await embed(chunk) for chunk in chunks]

    add_chunks(
        document_id=document_id,
        filename=file.filename or "unnamed",
        chunks=chunks,
        embeddings=embeddings,
    )

    return {
        "document_id": document_id,
        "filename": file.filename,
        "chunk_count": len(chunks),
    }
