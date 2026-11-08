from pathlib import Path
from pypdf import PdfReader


def load_pdf(file_path: str | Path):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Expected a file, got: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError("File must have a .pdf extension")

    documents = []

    try:
        reader = PdfReader(path)

        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")

        total_pages = len(reader.pages)

        for page_index, page in enumerate(reader.pages):

            raw_text = (page.extract_text() or "").strip()

            documents.append({
                "text": raw_text,
                "metadata": {
                    "source": str(path.resolve()),
                    "file_name": path.name,
                    "page": page_index + 1,
                    "total_pages": total_pages,
                    "status": "extracted" if raw_text else "empty",
                    "char_count": len(raw_text),
                }
            })

    except (FileNotFoundError, ValueError):
        raise

    except Exception as exc:
        raise RuntimeError(
            f"Failed to extract PDF: {path}"
        ) from exc

    return documents


if __name__ == "__main__":
    res = load_pdf("data/pdfs/RAG.pdf")
    print(res)
