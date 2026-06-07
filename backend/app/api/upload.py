from fastapi import APIRouter, UploadFile, File

from app.services.pdf_service import extract_text_from_pdf

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file.file)

    return {
        "filename": file.filename,
        "characters": len(text),
        "preview": text[:500]
    }