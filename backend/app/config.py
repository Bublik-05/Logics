"""
Minimal MVP configuration — deliberately small. No multi-provider abstraction,
no auth secrets, no DB connection strings: this MVP has none of those things.
When the project grows back toward the full v2 architecture, this file is
the one that gets split into app/config/settings.py again.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- Ollama (single LLM provider, no abstraction over alternatives) ---
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_CHAT_MODEL: str = "llama3"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"

    # --- ChromaDB ---
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION: str = "logics_mvp_chunks"

    # --- Storage ---
    STORAGE_PATH: str = "./data"

    # --- Chunking / retrieval ---
    CHUNK_SIZE_WORDS: int = 220
    CHUNK_OVERLAP_WORDS: int = 40
    TOP_K: int = 4


@lru_cache
def get_settings() -> Settings:
    return Settings()
