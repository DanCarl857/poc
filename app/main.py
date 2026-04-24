from fastapi import FastAPI, HTTPException

from app.db import init_db
from app.qa import QASystem
from app.schemas import AskRequest, AskResponse
from app.usage import get_clinic_usage
from app.openai_client import OpenAIError

app = FastAPI(title="Platform QA POC")

init_db()
qa_system = QASystem()


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/reindex")
def reindex():
    try:
        return {
            "status": "reloaded",
            **qa_system.reload(),
        }
    except OpenAIError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected indexing error")


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
    except OpenAIError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Unexpected server error")


@app.get("/admin/clinics/{clinic_key}/usage")
def clinic_usage(clinic_key: str):
    try:
        return get_clinic_usage(clinic_key)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/metrics")
def metrics():
    return {"status": "ok"}