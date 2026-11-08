import chromadb
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DB_PATH = BASE_DIR / "chroma_db"


client = chromadb.PersistentClient(
    path=str(CHROMA_DB_PATH)
)


collection = client.get_or_create_collection(
    name="persian_documents",
    metadata={"hnsw:space": "cosine"}
)


def add_chunks(embedded_chunks: list[dict]) -> None:

    if not embedded_chunks:
        return

    ids = [
        (
            f"{chunk['metadata']['source']}_"
            f"{chunk['metadata']['page']}_"
            f"{chunk['chunk_index']}"
        )
        for chunk in embedded_chunks
    ]

    documents = [
        chunk["text"]
        for chunk in embedded_chunks
    ]

    embeddings = [
        chunk["embedding"]
        for chunk in embedded_chunks
    ]

    metadatas = [
        {
            **chunk["metadata"],
            "chunk_index": chunk["chunk_index"]
        }
        for chunk in embedded_chunks
    ]

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search_chunks(
    query_embedding: list[float],
    n_results: int = 3
) -> dict:

    if not query_embedding:
        raise ValueError("Query embedding cannot be empty.")

    total_chunks = collection.count()

    if total_chunks == 0:
        return {
            "ids": [[]],
            "documents": [[]],
            "metadatas": [[]],
            "distances": [[]]
        }

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, total_chunks)
    )

    return results
