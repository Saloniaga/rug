def build_rag_prompt(
        question: str,
        context: str
):
    return f"""
You are a helpful assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, say:
"I could not find that information in the document."

Context:
{context}

Question:
{question}
"""