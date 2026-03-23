import Header from "./components/Header";
import UploadPDF from "./components/UploadPDF";
import ChatBox from "./components/ChatBox";

export default function App() {
  return (
    <div className="app">
      <Header />

      <main className="main-container">
        <section className="left-panel card">
          <h2 className="section-title">Upload Your PDF</h2>
          <p className="section-subtitle">
            Upload your study material and ask questions from it.
          </p>
          <UploadPDF />
        </section>

        <section className="right-panel card">
          <h2 className="section-title">Ask StudyMind AI</h2>
          <p className="section-subtitle">
            Ask anything from the uploaded PDF and get instant answers.
          </p>
          <ChatBox />
        </section>
      </main>
    </div>
  );
}