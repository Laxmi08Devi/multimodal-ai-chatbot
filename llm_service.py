from openai import OpenAI

from app.config import settings


client = OpenAI(
    api_key=settings.openai_api_key
)


def generate_response(
    message: str,
    context: str = ""
) -> str:

    if not settings.openai_api_key:
        return (
            "OpenAI API key is not configured. "
            "Please add OPENAI_API_KEY to your .env file."
        )

    prompt = message

    if context:
        prompt = f"""
Use the following retrieved information when answering.

CONTEXT:
{context}

USER QUESTION:
{message}

Answer clearly and only use the context when it is relevant.
"""

    response = client.responses.create(
        model=settings.openai_model,
        input=prompt
    )

    return response.output_text