from app.ingest import load_all_documents
from app.chunking import chunk_documents
from app.retriever import Retriever
from app.llm import build_prompt, call_openai
from app.schemas import AskResponse, SourceItem
from app.usage import (
    check_quota,
    reserve_question_slot,
    add_token_usage,
    get_usage_snapshot,
    log_chat_request,
    today_utc,
)

class QASystem:
    def __init__(self):
        self.documents = load_all_documents()
        self.chunks = chunk_documents(self.documents)
        self.retriever = Retriever(self.chunks)

    def reload(self):
        self.documents = load_all_documents()
        self.chunks = chunk_documents(self.documents)
        self.retriever = Retriever(self.chunks)

    def ask(self, clinic_key: str, question: str, top_k: int = 4, max_output_tokens: int = 300) -> AskResponse:
        clinic, usage = check_quota(clinic_key)
        usage_date = today_utc()

        reserve_question_slot(clinic["id"], usage_date)

        retrieved = self.retriever.search(question, top_k=top_k)
        context = [chunk.content for chunk in retrieved]

        prompt = build_prompt(question, context)
        result = call_openai(prompt, max_output_tokens=max_output_tokens)

        add_token_usage(clinic["id"], usage_date, result["total_tokens"])
        log_chat_request(
            clinic_id=clinic["id"],
            question=question,
            answer=result["text"],
            prompt_tokens=result["input_tokens"],
            completion_tokens=result["output_tokens"],
            total_tokens=result["total_tokens"],
        )

        clinic_after, usage_after = get_usage_snapshot(clinic["id"], usage_date)

        sources = [
            SourceItem(
                source=chunk.source,
                chunk_id=chunk.chunk_id,
                content=chunk.content,
            )
            for chunk in retrieved
        ]

        return AskResponse(
            answer=result["text"],
            sources=sources,
            questions_used_today=usage_after["questions_used"],
            questions_limit_today=clinic_after["daily_question_limit"],
            tokens_used_today=usage_after["tokens_used"],
            tokens_limit_today=clinic_after["daily_token_limit"],
        )