from fastapi import APIRouter

from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_service import ChatService


router = APIRouter(prefix="/api/chat", tags=["chat"])
chat_service = ChatService()


@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest) -> ChatResponse:
    return await chat_service.ask(request)
