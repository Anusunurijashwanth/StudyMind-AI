import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

VECTOR_PATH = "vector_store"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = OllamaLLM(
    model="phi3",
    base_url="http://127.0.0.1:11434"
)


def process_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    if not documents:
        return "PDF contains no readable content."

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    if not chunks:
        return "No text chunks created."

    vectorstore = FAISS.from_documents(chunks, embedding_model)

    os.makedirs(VECTOR_PATH, exist_ok=True)
    vectorstore.save_local(VECTOR_PATH)

    return "PDF processed successfully."


def is_pdf_related_question(question: str) -> bool:
    question = question.lower().strip()

    pdf_keywords = [
        "this pdf",
        "this document",
        "uploaded pdf",
        "uploaded file",
        "read this pdf",
        "read this document",
        "summarize this pdf",
        "summarize this document",
        "what is in this pdf",
        "what is in this document",
        "give me about this pdf",
        "explain this pdf",
        "tell me about this pdf",
        "contents of this pdf",
        "details in this pdf",
        "details in this document"
    ]

    for keyword in pdf_keywords:
        if keyword in question:
            return True

    return False


def general_answer(question: str):
    prompt = f"""
You are a helpful AI assistant.

Answer the following question clearly and correctly.

Question:
{question}

Answer:
"""
    return llm.invoke(prompt)


def pdf_answer(question: str):
    if not os.path.exists(VECTOR_PATH):
        return "No PDF has been uploaded yet."

    vectorstore = FAISS.load_local(
        VECTOR_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    docs_with_scores = vectorstore.similarity_search_with_score(question, k=4)

    if not docs_with_scores:
        return "I could not find relevant content in the uploaded PDF."

    best_score = docs_with_scores[0][1]

    context = "\n\n".join([doc.page_content for doc, _ in docs_with_scores])

    # If explicit PDF question, use PDF even if similarity is weak
    prompt = f"""
You are a helpful AI assistant.

The user is asking about the uploaded PDF.
Use the PDF context below to answer.
If the user asks to read, summarize, explain, or tell about the PDF,
give a concise summary of the uploaded PDF.
If the answer is not fully available, say what is available from the PDF.

Context:
{context}

Question:
{question}

Answer:
"""
    return llm.invoke(prompt)


def hybrid_answer(question: str):
    if not os.path.exists(VECTOR_PATH):
        return general_answer(question)

    vectorstore = FAISS.load_local(
        VECTOR_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    docs_with_scores = vectorstore.similarity_search_with_score(question, k=3)

    if not docs_with_scores:
        return general_answer(question)

    best_score = docs_with_scores[0][1]

    # Lower score = better PDF match
    if best_score <= 1.0:
        context = "\n\n".join([doc.page_content for doc, _ in docs_with_scores])

        prompt = f"""
You are a helpful AI assistant.

Use the PDF context below if it is relevant.
If the answer is clearly available in the PDF context, answer from it.
If the question is general and not really about the PDF, answer from your general knowledge.

Context:
{context}

Question:
{question}

Answer:
"""
        return llm.invoke(prompt)

    return general_answer(question)


def ask_question(question):
    try:
        question = question.strip()

        if not question:
            return "Please enter a valid question."

        # Explicit PDF-type question
        if is_pdf_related_question(question):
            return pdf_answer(question)

        # Otherwise choose between PDF/general intelligently
        return hybrid_answer(question)

    except Exception as e:
        return f"AI error: {str(e)}"