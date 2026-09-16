from pathlib import Path
from app.search.web_search import web_search
from app.web_agent import answer_web_question
from app.data_agent.agent import analyze_with_agent

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.rag import answer_question
from app.vector_store import build_vector_store


DOCUMENTS_DIR = Path("data/documents")

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATASETS_DIR = Path("data/datasets")
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="Enterprise AI Knowledge Copilot",
    description="AI-powered document question answering system",
    version="0.4.0"
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------
# Root
# --------------------------------

@app.get("/")
def root():
    return {
        "message":
        "Enterprise AI Knowledge Copilot API is running!"
    }


# --------------------------------
# Health
# --------------------------------

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------
# Ask AI
# --------------------------------

@app.get("/ask")
def ask_ai(
    question: str,
    conversation: str = ""
):
    return answer_question(
        question=question,
        conversation=conversation
    )

@app.get("/web-search")
def search_web(
    query: str
):
    return {
        "query": query,
        "results": web_search(query)
    }
@app.get("/web-ask")
def ask_web_ai(query: str):
    return answer_web_question(query)

@app.post("/data-upload")
async def upload_dataset(
    file: UploadFile = File(...)
):
    if not file.filename:
        return {
            "error": "No file selected."
        }

    if not file.filename.lower().endswith(".csv"):
        return {
            "error": "Only CSV files are supported."
        }

    file_path = (
        DATASETS_DIR
        / Path(file.filename).name
    )

    content = await file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file_path.name,
        "message": (
            "CSV uploaded successfully."
        )
    }
# --------------------------------
# Upload PDF
# --------------------------------

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # --------------------------------
    # Validate file type
    # --------------------------------

    if not file.filename:
        return {
            "error": "No file selected."
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error":
            "Only PDF files are supported."
        }

    # --------------------------------
    # Save PDF
    # --------------------------------

    file_path = (
        DOCUMENTS_DIR /
        Path(file.filename).name
    )

    content = await file.read()

    with open(
        file_path,
        "wb"
    ) as f:
        f.write(content)

    # --------------------------------
    # Build vector store
    # --------------------------------

    build_vector_store(
        str(file_path)
    )

    return {
        "filename": file_path.name,
        "message":
        "PDF uploaded and vector store updated successfully."
    }

@app.get("/data-ask")
def ask_data_ai(
    question: str,
    filename: str
):
    file_path = (
        DATASETS_DIR
        / Path(filename).name
    )

    if not file_path.exists():
        return {
            "error": "Dataset not found."
        }

    return analyze_with_agent(
        file_path=str(file_path),
        question=question
    )