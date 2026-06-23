from fastapi import APIRouter
from app.vectorstore.chroma_service import collection

router = APIRouter()

@router.get("/documents")
def get_documents():

    results = collection.get(
        include=["metadatas"]
    )

    filenames = set()

    for metadata in results["metadatas"]:
        filenames.add(
            metadata["filename"]
        )

    return sorted(list(filenames))