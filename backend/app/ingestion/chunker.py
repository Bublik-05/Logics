"""
Chunking. A simple fixed-size, word-based splitter with overlap — good enough
to make retrieval work. Swap for a smarter strategy later once you have a
golden set to actually measure whether "smarter" helps.
"""


def chunk_text(text: str, chunk_size_words: int, overlap_words: int) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    step = max(chunk_size_words - overlap_words, 1)

    for start in range(0, len(words), step):
        chunk_words = words[start : start + chunk_size_words]
        if not chunk_words:
            break
        chunks.append(" ".join(chunk_words))
        if start + chunk_size_words >= len(words):
            break

    return chunks
