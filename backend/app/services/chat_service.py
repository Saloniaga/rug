from openai import OpenAI
from dotenv import load_dotenv
import os
from app.services.retrieval_service import retrieve_context
from app.llm.prompts import build_system_prompt
from app.services.memory_service import (get_history,add_message)
from app.config import DEBUG

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def ask_question(
        session_id: str,
        question: str,
        filename: str
):

    retrieval_result = retrieve_context(
    query=question,
    filename=filename
    )
    context = retrieval_result["context"]
    sources = retrieval_result["sources"]

    system_prompt = build_system_prompt()

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "system",
            "content": f"""
            Context:{context}
            """
        }
    ]
    history = get_history(session_id)[-10:]
    if DEBUG:
        print("\nHISTORY:")
        print(history)

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )
    answer = response.choices[0].message.content

    add_message(
        session_id=session_id,
        role="user",
        content=question
    )

    add_message(
        session_id=session_id,
        role="assistant",
        content=answer
    )

    return {
        "answer": answer,
        "sources": sources
    }