"""
Chat — the core scenario: embed the question, retrieve matching chunks,
force the LLM to answer only from those chunks, and return the sources used.

No conversation history, no memory: every question is independent. That's the
right cut for the MVP — history is a real feature, but it's not what proves
the retrieval+citation loop works.
"""
from app.config import get_settings
from app.llm.ollama_client import embed, generate
from app.vectorstore.chroma_client import query

settings = get_settings()

PROMPT_TEMPLATE = """Ты — ассистент, который отвечает СТРОГО на основе предоставленных фрагментов документов.
Если ответа нет во фрагментах — прямо скажи, что в загруженных документах это не найдено.
Не используй никакие знания, кроме фрагментов ниже.

Фрагменты:
{context}

Вопрос: {question}

Ответ:"""


async def answer_question(question: str) -> dict:
    query_embedding = await embed(question)
    matches = query(query_embedding=query_embedding, top_k=settings.TOP_K)

    if not matches:
        return {
            "answer": "В загруженных документах пока ничего нет — сначала загрузите хотя бы один файл через /documents.",
            "sources": [],
        }

    context = "\n\n".join(
        f"[{i+1}] (источник: {m['filename']}, фрагмент №{m['chunk_index']})\n{m['content']}"
        for i, m in enumerate(matches)
    )

    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    answer = await generate(prompt)

    sources = [
        {
            "document_id": m["document_id"],
            "filename": m["filename"],
            "chunk_index": m["chunk_index"],
            "snippet": m["content"][:200],
        }
        for m in matches
    ]

    return {"answer": answer.strip(), "sources": sources}
