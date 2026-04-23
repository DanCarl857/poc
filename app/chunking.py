import re
from app.schemas import Document, Chunk


def split_markdown_sections(content: str) -> list[str]:
    parts = re.split(r"\n(?=#)", content)
    return [part.strip() for part in parts if part.strip()]


def chunk_documents(documents: list[Document]) -> list[Chunk]:
    chunks = []

    for doc in documents:
        if doc.doc_type == "markdown":
            parts = split_markdown_sections(doc.content)
        else:
            parts = [doc.content]

        for i, part in enumerate(parts):
            chunks.append(
                Chunk(
                    content=part,
                    source=doc.source,
                    doc_type=doc.doc_type,
                    chunk_id=f"{doc.source}::chunk_{i}",
                )
            )

    return chunks