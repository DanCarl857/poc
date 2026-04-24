import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DOCS_PATH = os.getenv("DOCS_PATH", "data/docs")
    OPENAPI_PATH = os.getenv("OPENAPI_PATH", "data/openapi.yaml")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


settings = Settings()