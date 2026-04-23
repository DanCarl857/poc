import requests
from app.config import settings

def build_prompt(question: str, context_chunks: list[str]) -> str:
    joined_context = "\n\n---\n\n".join(context_chunks)
    return f"""You are a platform support assistant.

Answer only from the provided context.
If the context does not support the answer, say you do not have enough information.

Question:
{question}

Context:
{joined_context}
"""

def call_openai(prompt: str, max_output_tokens: int = 300) -> dict:
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.OPENAI_MODEL,
            "input": prompt,
            "max_output_tokens": max_output_tokens,
        },
        timeout=60,
    )

    if response.status_code >= 400:
        raise RuntimeError(f"OpenAI error {response.status_code}: {response.text}")

    data = response.json()
    output_text = data.get("output_text", "")

    usage = data.get("usage", {}) or {}
    input_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    total_tokens = usage.get("total_tokens", input_tokens + output_tokens)

    return {
        "text": output_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
    }