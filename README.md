#  StudyMind AI Assistant

An AI-powered PDF Question Answering System that allows users to upload study materials and ask questions from them, along with general AI knowledge support.

---

##  Tech Stack

###  Frontend

* React.js

###  Backend

* Spring Boot (Java)

###  AI Service

* FastAPI (Python)
* LangChain
* FAISS (Vector Database)
* HuggingFace Embeddings
* Ollama (phi3 model)

###  Database

* MongoDB

---

##  Features

*  Upload PDF files
*  Ask questions from uploaded PDF
*  AI answers from document context
*  General knowledge Q&A (outside PDF)
*  Offline AI using Ollama (phi3)
*  Stores chat history in MongoDB

---

##  Architecture

React Frontend → Spring Boot → FastAPI → FAISS + Ollama
                                                                       ↓
                                                                       MongoDB

---

##  Project Structure

```
StudyMind-AI/
│
├── studymind-frontend/   # React App
├── spring-backend/       # Spring Boot API
├── ai-service/           # FastAPI AI Service
├── .gitignore
└── README.md
```

---

##  Setup & Run

### 1 Start MongoDB

```bash
mongod --dbpath C:\data\db
```

---

### 2️ Start Ollama (AI Model)

```bash
ollama serve
```

Then run model:

```bash
ollama run phi3
```

---

### 3️ Run FastAPI (AI Service)

```bash
cd ai-service
python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

 Runs on:
 http://127.0.0.1:8000

---

### 4️ Run Spring Boot Backend

```bash
cd spring-backend
mvn spring-boot:run
```

👉 Runs on:
📍 http://localhost:8080

---

### 5️ Run React Frontend

```bash
cd studymind-frontend
npm install
npm start
```

 Runs on:
 http://localhost:3000

---

##  API Endpoints

###  Upload PDF

```
POST /api/ai/upload
```

###  Ask Question

```
GET /api/ai/ask?question=your_question
```

###  Check Status

```
GET /api/ai/status
```

---

##  How It Works

1. User uploads a PDF
2. FastAPI processes and stores embeddings using FAISS
3. User asks a question
4. System:

   * Searches PDF context
   * If found → answers from PDF
   * If not → answers using AI model
5. Response stored in MongoDB

---

##  Example Questions

* "What is this PDF about?"
* "Explain Unit 2 concepts"
* "What is Python?"
* "Java roadmap"

---

##  Notes

* Ensure all services are running before using the app
* Large PDFs may take time to process (handled in background)
* Works offline with Ollama (no internet required after setup)

---

##  Future Enhancements

*  User authentication
*  Chat history UI
*  Mobile app version
*  Voice input support
*  Cloud deployment

---

##  Author

**Anusunuri Jashwanth**
B.Tech Student

---

##  If you like this project

Give it a  on GitHub!
