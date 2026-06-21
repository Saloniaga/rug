from fastapi import APIRouter

from app.models.chat_request import ChatRequest
from app.services.chat_service import ask_question

router = APIRouter()


@router.post("/chat")
async def chat(request: ChatRequest):

    return ask_question(
        request.question
    )
    