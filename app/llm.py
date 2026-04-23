import json
import requests
import boto3

from app.config import settings


def build_prompt(question: str, context_chunks: list[str]) -> str:
    joined_context = "\n\n---\n\n".join(context_chunks)

    return f"""You are a platform support assistant.

Answer the user's question using only the provided context.
If the answer is not supported by the context, say you do not have enough information.

Question:
{question}

Context:
{joined_context}

Answer:
"""


def call_mock_llm(prompt: str) -> str:
    return f"[MOCK ANSWER]\\n\\nThis is where the model answer would go.\\n\\nPrompt excerpt:\\n{prompt[:1000]}"


def call_openai_compatible(prompt: str) -> str:
    response = requests.post(
        f"{settings.OPENAI_BASE_URL}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.OPENAI_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


def call_bedrock(prompt: str) -> str:
    client = boto3.client("bedrock-runtime", region_name=settings.AWS_REGION)

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 800,
        "temperature": 0.2,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    response = client.invoke_model(
        modelId=settings.BEDROCK_MODEL_ID,
        body=json.dumps(body),
    )

    raw = response["body"].read()
    data = json.loads(raw)
    return data["content"][0]["text"]


def answer_question(question: str, context_chunks: list[str]) -> str:
    prompt = build_prompt(question, context_chunks)

    if settings.LLM_PROVIDER == "bedrock":
        return call_bedrock(prompt)

    if settings.LLM_PROVIDER == "openai_compatible":
        return call_openai_compatible(prompt)

    return call_mock_llm(prompt)