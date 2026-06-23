"use client";

import { useState, useRef, useEffect } from "react";

type Source = {
  filename: string;
  chunk_number: number;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<Message[]>([]);

  const [sessionId] = useState(crypto.randomUUID());

  const bottomRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
    bottomRef.current?.scrollIntoView({
        behavior: "smooth"
    });
    }, [messages]);

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
      "http://localhost:8000/upload",
      {
        method: "POST",
        body: formData,
      }
    );

    const data = await response.json();

    console.log(data);

    alert("Upload successful!");
  };

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    const userQuestion = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");

    const response = await fetch(
      "http://localhost:8000/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          question: userQuestion,
          filename: "SaloniAgar_0626_SWE.pdf"
        }),
      }
    );

    const data = await response.json();

    console.log(data);

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: data.answer,
        sources: data.sources
      },
    ]);
  };


    const askQuestionStream = async () => {

  if (!question.trim()) {
    return;
  }

  const userQuestion = question;

  setMessages(prev => [
    ...prev,
    {
      role: "user",
      content: userQuestion
    }
  ]);

  setQuestion("");

  const response = await fetch(
    "http://localhost:8000/chat/stream",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: sessionId,
        question: userQuestion,
        filename: "SaloniAgar_0626_SWE.pdf"
      })
    }
  );

  if (!response.body) {
    return;
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder();

  let assistantAnswer = "";

  setMessages(prev => [
    ...prev,
    {
      role: "assistant",
      content: ""
    }
  ]);

  while (true) {

    const { done, value } =
      await reader.read();

    if (done) {
      break;
    }

    const chunk =
      decoder.decode(value);

    assistantAnswer += chunk;

    setMessages(prev => {

      const updated = [...prev];

      updated[updated.length - 1] = {
        role: "assistant",
        content: assistantAnswer
      };

      return updated;
    });
  }
};


  return (
    <main className="p-10 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">
        PDF RAG Assistant
      </h1>

      <div className="mb-8">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            if (e.target.files?.[0]) {
              setFile(e.target.files[0]);
            }
          }}
        />

        <button
          onClick={uploadFile}
          className="ml-4 border px-4 py-2 rounded"
        >
          Upload
        </button>
      </div>

      <div className="space-y-4 mb-8">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`p-3 rounded max-w-2xl ${
              message.role === "user"
                ? "bg-blue-600 ml-auto"
                : "bg-gray-800"
            }`}
          >
            <div className="font-bold mb-1">
              {message.role === "user"
                ? "You"
                : "Assistant"}
            </div>

            <div>{message.content}</div>

            {
            message.sources &&
            message.sources.length > 0 && (
                <div className="mt-2 text-sm text-gray-300">

                <div className="font-bold">
                    Sources
                </div>

                {
                    message.sources.map(
                    (source, index) => (
                        <div key={index}>
                        {source.filename}
                        {" "}
                        (chunk {source.chunk_number})
                        </div>
                    )
                    )
                }

                </div>
            )
            }
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question..."
          className="flex-1 border p-2 rounded bg-white text-black"
        />

        <button
          onClick={askQuestion}
          className="border px-4 py-2 rounded"
        >
          Send
        </button>
        <button
            onClick={askQuestionStream}
            className="border px-4 py-2 rounded ml-2"
        >
            Stream
        </button>
      </div>
    </main>
  );
}