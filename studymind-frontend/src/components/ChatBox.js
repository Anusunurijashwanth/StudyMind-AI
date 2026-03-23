import { useState } from "react";
import { askAI, getStatus } from "../services/api";
import Message from "./Message";

export default function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!question.trim()) return;

    const q = question.trim();

    setMessages((prev) => [...prev, { type: "user", text: q }]);
    setQuestion("");
    setLoading(true);

    try {
      const status = await getStatus();

      if (!status.ready) {
        setMessages((prev) => [
          ...prev,
          {
            type: "ai",
            text: "⏳ PDF is still processing. Please wait a few seconds and try again."
          }
        ]);
        return;
      }

      const data = await askAI(q);

      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: data?.answer || "No response received"
        }
      ]);
    } catch (error) {
      console.error("Ask error:", error);
      setMessages((prev) => [
        ...prev,
        {
          type: "ai",
          text: "Error getting response"
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-messages">
        {messages.map((m, i) => (
          <Message key={i} msg={m} />
        ))}
        {loading && <p className="thinking">AI is thinking...</p>}
      </div>

      <div className="chat-input-row">
        <input
          className="chat-input"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask anything..."
          onKeyDown={(e) => {
            if (e.key === "Enter") send();
          }}
        />
        <button className="ask-btn" onClick={send}>
          Ask
        </button>
      </div>
    </div>
  );
}