import os
import shutil
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from rag_service import process_pdf, ask_question

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

PDF_READY = False


def background_process_pdf(file_path: str):
    global PDF_READY
    PDF_READY = False
    process_pdf(file_path)
    PDF_READY = True


@app.get("/")
def home():
    return {"message": "StudyMind AI Service Running"}


@app.get("/status")
def status():
    return {"ready": PDF_READY}


@app.post("/upload")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    background_tasks.add_task(background_process_pdf, file_path)

    return {"status": "PDF uploaded successfully. Processing started in background."}


@app.get("/ask")
def ask(question: str):
    if not PDF_READY:
        return {"answer": "⏳ PDF is still processing. Please wait a few seconds and try again."}

    try:
        answer = ask_question(question)
        return {"answer": answer}
    except Exception as e:
        return {"answer": f"Server error: {str(e)}"}