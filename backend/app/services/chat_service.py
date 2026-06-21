from openai import OpenAI
from dotenv import load_dotenv
import os
from app.services.retrieval_service import retrieve_context
from app.llm.prompts import build_rag_prompt

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_question(question: str):

    retrieval_result = retrieve_context(question)
    context = retrieval_result["context"]
    sources = retrieval_result["sources"]

    prompt = build_rag_prompt(
        question=question,
        context=context
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": sources
    }