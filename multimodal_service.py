import base64
from pathlib import Path

from openai import OpenAI

from app.config import settings


client = OpenAI(
    api_key=settings.openai_api_key
)


def analyze_image(
    file_path: str,
    question: str
) -> str:

    if not settings.openai_api_key:
        return (
            "OpenAI API key is not configured."
        )

    extension = Path(
        file_path
    ).suffix.lower()

    mime_type = "image/jpeg"

    if extension == ".png":
        mime_type = "image/png"

    elif extension == ".webp":
        mime_type = "image/webp"

    with open(
        file_path,
        "rb"
    ) as image_file:

        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    image_url = (
        f"data:{mime_type};base64,"
        f"{image_data}"
    )

    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": question
                    },
                    {
                        "type": "input_image",
                        "image_url": image_url
                    }
                ]
            }
        ]
    )

    return response.output_text