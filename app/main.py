from fastapi import FastAPI
from app.qa import QASystem
from app.schemas import AskRequest, AskResponse

app = FastAPI(title="Platform QA POC")

qa_system = QASystem()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "documents": len(qa_system.documents),
        "chunks": len(qa_system.chunks),
    }

@app.post("/reindex")
def reindex():
    qa_system.reload()
    return {
        "status": "reloaded",
        "documents": len(qa_system.documents),
        "chunks": len(qa_system.chunks),
    }


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    return qa_system.ask(request.question, top_k=request.top_k)