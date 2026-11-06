
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> list[dict]:

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

        text_chunks = splitter.split_text(text)

        for index, chunk in enumerate(text_chunks):
            chunks.append({
                "text": chunk,
                "chunk_index": index,
                "metadata": metadata,
            })

    return chunks