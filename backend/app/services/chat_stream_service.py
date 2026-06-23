from openai import OpenAI
from dotenv import load_dotenv
import os

from app.services.retrieval_service import retrieve_context
from app.llm.prompts import build_system_prompt
from app.services.memory_service import add_message, get_history

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_question_stream(
        session_id: str,
        question: str,
        filename: str
):
    retrieval_result = retrieve_context(
    query=question,
    filename=filename
)

    context = retrieval_result["context"]

    history = get_history(session_id)[-10:]

    messages = [
        {
            "role": "system",
            "content": build_system_prompt()
        },
        {
            "role": "system",
            "content": f"Context:\n\n{context}"
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )
    full_answer = ""
    for chunk in stream:
        delta = chunk.choices[0].delta.content

        if delta:
            full_answer += delta;
            yield delta
    
    add_message(session_id, "user", question)
    add_message(session_id, "assistant", full_answer)