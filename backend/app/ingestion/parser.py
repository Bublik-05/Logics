"""
Text extraction. One function, one job — no Parser interface/registry.
Supports PDF and plain text, which covers the MVP scenario end to end.
Add DOCX/OCR later by extending this function, not by building an abstraction first.
"""
from pathlib import Path

from pypdf import PdfReader


def extract_text(file_path: str, mime_type: str) -> str:
    """Extract raw text from a PDF or plain-text file."""
    path = Path(file_path)

    if mime_type == "application/pdf" or path.suffix.lower() == ".pdf":
        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    # Fallback: treat anything else as plain text.
    return path.read_text(encoding="utf-8", errors="ignore")
