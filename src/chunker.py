from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            "؟",
            ".",
            "!",
            "؛",
            "،",
            " ",
            "",
        ],
        length_function=len,
        is_separator_regex=False,
    )

    chunks = []

    for document in documents:

        text = document["text"]
        metadata = document["metadata"]

        if not text.strip():
            continue

        text_chunks = splitter.split_text(text)

        for index, chunk in enumerate(text_chunks):

            chunks.append({
                "text": chunk,
                "chunk_index": index,
                "metadata": metadata.copy(),
            })

    return chunks