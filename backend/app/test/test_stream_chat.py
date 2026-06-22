from app.services.chat_stream_service import ask_question_stream

for chunk in ask_question_stream(
    session_id="test",
    question="What databases has Saloni worked on?"
):
    print(chunk, end="", flush=True)