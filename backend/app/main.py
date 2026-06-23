from fastapi import FastAPI
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.chat_stream import (
    router as chat_stream_router
)
from app.api.documents import router as documents_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(chat_stream_router)
app.include_router(documents_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "PDF RAG Backend is up"
    }