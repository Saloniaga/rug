# app/services/retrieval_service.py

from app.services.embedding_service import create_embedding
from app.vectorstore.chroma_service import search
from app.config import DEBUG


def retrieve_context(
        query: str,
        n_results: int = 5
):
    query_embedding = create_embedding(query)

    results = search(
        embedding=query_embedding,
        n_results=n_results
    )
    if DEBUG:
        print("\n")
        print("=" * 100)
        print("QUERY:", query)
        print("=" * 100)


    documents = results["documents"][0]
    distances = results["distances"][0]
    metadatas = results["metadatas"][0]

    if DEBUG:
        for doc, distance, metadata in zip(
                documents,
                distances,
                metadatas
        ):
            print("\n")
            print("-" * 80)
            print("Distance:", distance)
            print("Metadata:", metadata)
            print("Preview:")
            print(doc[:250])

    # good_chunks = []

    # for doc, distance in zip(documents, distances):
    #     if distance < 1.2:
    #         good_chunks.append(doc)

    return {
        "context": "\n\n".join(documents),
        "sources": metadatas
    }
