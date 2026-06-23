from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.chat_request import ChatRequest
from app.services.chat_stream_service import (
    ask_question_stream
)

router = APIRouter()

@router.post("/chat/stream")
async def chat_stream(
        request: ChatRequest
):

    generator = ask_question_stream(
        session_id=request.session_id,
        question=request.question,
        filename=request.filename
    )

    return StreamingResponse(
        generator,
        media_type="text/plain"
    )