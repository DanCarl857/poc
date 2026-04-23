from pathlib import Path
import yaml

from app.config import settings
from app.schemas import Document

def load_markdown_docs() -> list[Document]:
    docs = []
    docs_path = Path(settings.DOCS_PATH)

    for file_path in docs.path.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        docs.append(
            Document(
                content=content,
                source=file_path.name,
                doc_type="markdown"
            )
        )

    return docs

def load_openapi_doc() -> list[Document]:
    openapi_path = Path(settings.OPENAPI_PATH)
    if not openapi_path.exists():
        return []
    
    raw = yaml.safe_load(openapi_path.read_text(encoding="utf-8"))

    docs = []
    paths = raw.get("paths", {})

    for path_name, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            description = details.get("description", "")

            text = f"""
Path: {path_name}
Method: {method.upper()}
Summary: {summary}
Description: {description}
""".strip()

            docs.append(
                Document(
                    content=text,
                    source=f"openapi:{method.upper()} {path_name}",
                    doc_type="openapi",
                )
            )

    return docs


def load_all_documents() -> list[Document]:
    return load_markdown_docs() + load_openapi_doc()