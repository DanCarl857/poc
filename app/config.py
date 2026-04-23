import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DOCS_PATH = os.getenv("DOCS_PATH", "data/docs")
    OPENAPI_PATH = os.getenv("OPENAPI_PATH", "data/openapi.yaml")

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "")

settings = Settings()