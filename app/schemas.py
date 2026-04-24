from pydantic import BaseModel
from typing import List


class Document(BaseModel):
    content: str
    source: str
    doc_type: str


class Chunk(BaseModel):
    content: str
    source: str
    doc_type: str
    chunk_id: str


class StoredChunk(Chunk):
    embedding: list[float]


class AskRequest(BaseModel):
    clinic_key: str
    question: str
    top_k: int = 4
    max_output_tokens: int = 300


class SourceItem(BaseModel):
    source: str
    chunk_id: str
    content: str


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceItem]
    cached: bool
    questions_used_today: int
    questions_limit_today: int
    tokens_used_today: int
    tokens_limit_today: int