from typing import Optional

import chromadb

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def add_document(
        doc_id: str,
        chunk: str,
        embedding: list,
        metadata: dict
):
    collection.add(
        ids=[doc_id],
        documents=[chunk],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def search(
        embedding: list,
        n_results: int = 5,
        filename: Optional[str] = None
):
    query_params = {
        "query_embeddings": [embedding],
        "n_results": n_results,
        "include": [
            "documents",
            "metadatas",
            "distances"
        ]
    }

    if filename:
        query_params["where"] = {
            "filename": filename
        }

    return collection.query(**query_params)