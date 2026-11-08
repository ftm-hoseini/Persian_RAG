from .embedding import get_embedding
from .vector_store import search_chunks


def retrieve_context(
    question: str,
    n_results: int = 3
) -> dict:

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if n_results < 1:
        raise ValueError("n_results must be at least 1.")

    
    query_embedding = get_embedding(question)

    
    results = search_chunks(
        query_embedding=query_embedding,
        n_results=n_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    context_parts = []
    sources = []
    seen_sources = set()

    for document, metadata in zip(documents, metadatas):

        file_name = metadata.get("file_name", "Unknown")
        page = metadata.get("page", "Unknown")
        source = metadata.get("source", file_name)

        context_parts.append(
            f"[منبع: {file_name}، صفحه: {page}]\n{document}"
        )

        source_key = (source, page)

        if source_key not in seen_sources:

            sources.append({
                "file_name": file_name,
                "page": page,
                "source": source
            })

            seen_sources.add(source_key)

    return {
        "context": "\n\n".join(context_parts),
        "sources": sources,
        "distances": distances
    }