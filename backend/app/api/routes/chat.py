"""
Single endpoint: ask a question, get an answer grounded in uploaded documents,
with the exact chunks used to produce it.
"""
from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import answer_question

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    result = await answer_question(request.question)
    return ChatResponse(**result)
