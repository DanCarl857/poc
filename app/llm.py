from app.openai_client import create_response


def build_prompt(question: str, context_chunks: list[str]) -> str:
    joined_context = "\n\n---\n\n".join(context_chunks)

    return f"""You are a platform support assistant.

Rules:
- Answer only from the provided context.
- If the context does not support the answer, say: "I do not have enough information from the documentation to answer that."
- Keep the answer concise.
- Do not invent platform features or rules.

Question:
{question}

Context:
{joined_context}

Answer:
"""


def answer_question(question: str, context_chunks: list[str], max_output_tokens: int = 300) -> dict:
    prompt = build_prompt(question, context_chunks)
    return create_response(prompt, max_output_tokens=max_output_tokens)