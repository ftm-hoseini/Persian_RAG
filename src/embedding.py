import requests
import os
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_API_URL = os.getenv("EMBEDDING_API_URL")


def get_embedding(text: str) -> list[float]:

    if not text.strip():
        raise ValueError("Cannot generate embedding for empty text.")

    try:
        response = requests.post(
            EMBEDDING_API_URL,
            json={"input": text},
            timeout=60,
        )

        response.raise_for_status()

        result = response.json()

        embedding = result["data"][0]["embedding"]

        if not isinstance(embedding, list) or not embedding:
            raise ValueError("Invalid embedding returned by API.")

        return embedding

    except requests.RequestException as exc:
        raise RuntimeError("Embedding API request failed.") from exc

    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError(
            "Unexpected embedding API response format."
        ) from exc



def embed_documents(chunks: list[dict]) -> list[dict]:

    embedded_chunks = []

    for chunk in chunks:

        embedding = get_embedding(chunk["text"])

        embedded_chunks.append({
            **chunk,
            "embedding": embedding,
        })

    return embedded_chunks
