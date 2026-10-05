"""
Single LLM provider client — deliberately not behind a swappable-provider
interface. If you later need OpenAI/LM Studio too, that's the moment to
introduce an abstraction, backed by two real implementations, not before.
"""
import httpx

from app.config import get_settings

settings = get_settings()


async def embed(text: str) -> list[float]:
    """Get an embedding vector for a single piece of text via Ollama's /api/embeddings."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/embeddings",
            json={"model": settings.OLLAMA_EMBED_MODEL, "prompt": text},
        )
        response.raise_for_status()
        return response.json()["embedding"]


async def generate(prompt: str) -> str:
    """Get a completion for a prompt via Ollama's /api/generate (non-streaming)."""
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{settings.OLLAMA_BASE_URL}/api/generate",
            json={"model": settings.OLLAMA_CHAT_MODEL, "prompt": prompt, "stream": False},
        )
        response.raise_for_status()
        return response.json()["response"]
