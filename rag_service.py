import math
from typing import List

from openai import OpenAI

from app.config import settings


client = OpenAI(
    api_key=settings.openai_api_key
)


def chunk_text(
    text: str,
    chunk_size: int = 800
) -> List[str]:

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):
        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def create_embedding(text: str):

    response = client.embeddings.create(
        model=settings.embedding_model,
        input=text
    )

    return response.data[0].embedding


def cosine_similarity(a, b):

    dot_product = sum(
        x * y
        for x, y in zip(a, b)
    )

    magnitude_a = math.sqrt(
        sum(x * x for x in a)
    )

    magnitude_b = math.sqrt(
        sum(x * x for x in b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (
        magnitude_a * magnitude_b
    )


def retrieve_relevant_chunks(
    query_embedding,
    chunks,
    top_k=3
):

    scored = []

    for chunk in chunks:

        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        scored.append(
            (score, chunk["text"])
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        text
        for score, text
        in scored[:top_k]
    ]