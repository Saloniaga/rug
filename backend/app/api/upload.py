from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import extract_text_from_pdf
from app.services.indexing_service import index_document

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)

    index_document(
        filename=file.filename,
        text=text
    )

    return {
        "message": "Document indexed successfully",
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:500]
    }