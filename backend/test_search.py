from app.services.embedding_service import create_embedding
from app.vectorstore.chroma_service import search

query = "What is this document about?"

embedding = create_embedding(query)

results = search(
    embedding=embedding,
    n_results=5
)

print(results["documents"])
print(results["metadatas"])