from fastapi import FastAPI
from app.api.upload import router as upload_router

app = FastAPI()

app.include_router(upload_router)


@app.get("/")
def health_check():
    return {
        "status": "running",
        "message": "PDF RAG Backend is up"
    }