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
