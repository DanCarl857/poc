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

class AskRequest(BaseModel):
    question: str
    top_k: int = 5

class SourceItem(BaseModel):
    source: str
    chunk_id: str
    content: str

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceItem]