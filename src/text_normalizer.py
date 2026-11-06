from piraye import NormalizerBuilder


normalizer = (
    NormalizerBuilder()
    .alphabet_fa()
    .digit_fa()
    .punctuation_fa()
    .remove_extra_spaces()
    .build()
)


def normalize_text(text: str) -> str:
    normalized_text, _ = normalizer.normalize(text)
    return normalized_text


def normalize_documents(documents: list[dict]) -> list[dict]:
    normalized_documents = []

    for document in documents:
        normalized_text = normalize_text(document["text"])

        normalized_documents.append({
            **document,
            "text": normalized_text,
        })

    return normalized_documents