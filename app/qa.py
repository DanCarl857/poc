from app.ingest import load_all_documents
from app.chunking import chunk_documents
from app.retriever import Retriever
from app.llm import answer_question
from app.schemas import AskResponse, SourceItem
from app.usage import (
    check_quota,
    increment_successful_usage,
    get_usage_snapshot,
    log_chat_request,
    today_utc,
    get_cached_answer,
    save_cached_answer,
)


class QASystem:
    def __init__(self):
        self.retriever = Retriever()
        self.documents = []
        self.chunks = []

    def reload(self):
        self.documents = load_all_documents()
        self.chunks = chunk_documents(self.documents)
        indexed_count = self.retriever.rebuild_index(self.chunks)

        return {
            "documents": len(self.documents),
            "chunks": len(self.chunks),
            "indexed": indexed_count,
        }

    def ask(
        self,
        clinic_key: str,
        question: str,
        top_k: int = 4,
        max_output_tokens: int = 300,
    ) -> AskResponse:
        clinic, usage = check_quota(clinic_key)
        usage_date = today_utc()

        cached = get_cached_answer(clinic["id"], question)

        if cached:
            clinic_after, usage_after = get_usage_snapshot(clinic["id"], usage_date)

            return AskResponse(
                answer=cached["answer"],
                sources=[SourceItem(**source) for source in cached["sources"]],
                cached=True,
                questions_used_today=usage_after["questions_used"],
                questions_limit_today=clinic_after["daily_question_limit"],
                tokens_used_today=usage_after["tokens_used"],
                tokens_limit_today=clinic_after["daily_token_limit"],
            )

        retrieved = self.retriever.search(question, top_k=top_k)

        if not retrieved:
            clinic_after, usage_after = get_usage_snapshot(clinic["id"], usage_date)

            return AskResponse(
                answer="I do not have enough information from the documentation to answer that.",
                sources=[],
                cached=False,
                questions_used_today=usage_after["questions_used"],
                questions_limit_today=clinic_after["daily_question_limit"],
                tokens_used_today=usage_after["tokens_used"],
                tokens_limit_today=clinic_after["daily_token_limit"],
            )

        context = [chunk.content for chunk in retrieved]

        try:
            result = answer_question(
                question=question,
                context_chunks=context,
                max_output_tokens=max_output_tokens,
            )

            increment_successful_usage(
                clinic_id=clinic["id"],
                usage_date=usage_date,
                total_tokens=result["total_tokens"],
            )

            sources = [
                SourceItem(
                    source=chunk.source,
                    chunk_id=chunk.chunk_id,
                    content=chunk.content,
                )
                for chunk in retrieved
            ]

            source_dicts = [source.model_dump() for source in sources]

            save_cached_answer(
                clinic_id=clinic["id"],
                question=question,
                answer=result["text"],
                sources=source_dicts,
            )

            log_chat_request(
                clinic_id=clinic["id"],
                question=question,
                answer=result["text"],
                prompt_tokens=result["input_tokens"],
                completion_tokens=result["output_tokens"],
                total_tokens=result["total_tokens"],
                success=True,
            )

            clinic_after, usage_after = get_usage_snapshot(clinic["id"], usage_date)

            return AskResponse(
                answer=result["text"],
                sources=sources,
                cached=False,
                questions_used_today=usage_after["questions_used"],
                questions_limit_today=clinic_after["daily_question_limit"],
                tokens_used_today=usage_after["tokens_used"],
                tokens_limit_today=clinic_after["daily_token_limit"],
            )

        except Exception as e:
            log_chat_request(
                clinic_id=clinic["id"],
                question=question,
                answer=None,
                success=False,
                error_message=str(e),
            )
            raise