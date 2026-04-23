from app.ingest import load_all_documents
from app.chunking import chunk_documents
from app.retriever import Retriever
from app.llm import answer_question
from app.schemas import AskResponse, SourceItem


class QASystem:
    def __init__(self):
        self.documents = load_all_documents()
        self.chunks = chunk_documents(self.documents)
        self.retriever = Retriever(self.chunks)

    def reload(self):
        self.documents = load_all_documents()
        self.chunks = chunk_documents(self.documents)
        self.retriever = Retriever(self.chunks)

    def ask(self, question: str, top_k: int = 5) -> AskResponse:
        retrieved = self.retriever.search(question, top_k=top_k)
        context = [chunk.content for chunk in retrieved]

        answer = answer_question(question, context)

        sources = [
            SourceItem(
                source=chunk.source,
                chunk_id=chunk.chunk_id,
                content=chunk.content,
            )
            for chunk in retrieved
        ]

        return AskResponse(answer=answer, sources=sources)