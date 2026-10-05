"""
MVP entrypoint. One purpose: upload a document, ask a question about it,
get an answer with a citation. No lifespan hooks, no middleware stack —
those come back when there's something real for them to do.
"""
from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(title="L.O.G.I.C.S. MVP", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")
