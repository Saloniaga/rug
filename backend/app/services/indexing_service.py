from app.services.chunk_service import chunk_text
from app.services.embedding_service import create_embedding
from app.vectorstore.chroma_service import add_document


def index_document(
        filename: str,
        text: str
):
    chunks = chunk_text(text)
    print("Chunk Count:", len(chunks))
    for i, chunk in enumerate(chunks):
        print("Indexing chunk", i)
        embedding = create_embedding(chunk)

        add_document(
            doc_id=f"{filename}_{i}",
            chunk=chunk,
            embedding=embedding,
            metadata={
                "filename": filename,
                "chunk_number": i
            }
        )
    print("Finished indexing")