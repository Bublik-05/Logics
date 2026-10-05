"""
Thin wrapper around a single ChromaDB collection. No metadata layer in Postgres —
for the MVP, ChromaDB's own metadata fields (document_id, filename, chunk_index)
are the only "database" this project has. That's a deliberate simplification:
add Postgres back only when you need something Chroma's metadata can't give you
(user accounts, document versions, audit history).
"""
import chromadb

from app.config import get_settings

settings = get_settings()

_client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
_collection = _client.get_or_create_collection(name=settings.CHROMA_COLLECTION)


def add_chunks(
    *, document_id: str, filename: str, chunks: list[str], embeddings: list[list[float]]
) -> None:
    ids = [f"{document_id}:{i}" for i in range(len(chunks))]
    metadatas = [
        {"document_id": document_id, "filename": filename, "chunk_index": i}
        for i in range(len(chunks))
    ]
    _collection.add(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)


def query(*, query_embedding: list[float], top_k: int) -> list[dict]:
    """Returns top_k matches as [{content, document_id, filename, chunk_index, distance}, ...]."""
    results = _collection.query(query_embeddings=[query_embedding], n_results=top_k)

    matches = []
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for content, metadata, distance in zip(documents, metadatas, distances):
        matches.append(
            {
                "content": content,
                "document_id": metadata.get("document_id"),
                "filename": metadata.get("filename"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distance,
            }
        )
    return matches
