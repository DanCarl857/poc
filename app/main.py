from fastapi import FastAPI, HTTPException
from app.qa import QASystem
from app.schemas import AskRequest, AskResponse
from app.db import init_db

app = FastAPI(title="Platform QA POC")

init_db()
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
    try:
        return qa_system.ask(
            clinic_key=request.clinic_key,
            question=request.question,
            top_k=request.top_k,
            max_output_tokens=request.max_output_tokens,
        )
    except ValueError as e:
        raise HTTPException(status_code=429, detail=str(e))