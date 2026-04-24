import json
import math
from datetime import datetime, timezone

from app.db import get_conn
from app.openai_client import create_embedding
from app.schemas import Chunk, StoredChunk


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


class Retriever:
    def __init__(self):
        pass

    def rebuild_index(self, chunks: list[Chunk]) -> int:
        now = datetime.now(timezone.utc).isoformat()

        with get_conn() as conn:
            conn.execute("DELETE FROM document_chunks")

            for chunk in chunks:
                embedding_result = create_embedding(chunk.content)
                embedding_json = json.dumps(embedding_result["embedding"])

                conn.execute(
                    """
                    INSERT INTO document_chunks (
                        chunk_id, source, doc_type, content, embedding_json, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk.chunk_id,
                        chunk.source,
                        chunk.doc_type,
                        chunk.content,
                        embedding_json,
                        now,
                    ),
                )

            conn.commit()

        return len(chunks)

    def load_chunks(self) -> list[StoredChunk]:
        with get_conn() as conn:
            rows = conn.execute(
                """
                SELECT chunk_id, source, doc_type, content, embedding_json
                FROM document_chunks
                """
            ).fetchall()

        return [
            StoredChunk(
                chunk_id=row["chunk_id"],
                source=row["source"],
                doc_type=row["doc_type"],
                content=row["content"],
                embedding=json.loads(row["embedding_json"]),
            )
            for row in rows
        ]

    def search(self, question: str, top_k: int = 4) -> list[StoredChunk]:
        embedding_result = create_embedding(question)
        query_embedding = embedding_result["embedding"]

        chunks = self.load_chunks()

        scored = [
            (cosine_similarity(query_embedding, chunk.embedding), chunk)
            for chunk in chunks
        ]

        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            chunk
            for score, chunk in scored[:top_k]
            if score > 0.1
        ]