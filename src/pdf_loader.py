from pathlib import Path
import pymupdf


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
        with pymupdf.open(path) as pdf:

            if pdf.is_encrypted:
                raise ValueError("Encrypted PDFs are not supported.")

            for page_index, page in enumerate(pdf):

                raw_text = page.get_text("text", sort=True).strip()

                documents.append({
                    "raw_text": raw_text,
                    "page_content": raw_text,
                    "metadata": {
                        "source": str(path.resolve()),
                        "file_name": path.name,
                        "page": page_index + 1,
                        "total_pages": pdf.page_count,
                        "status": "extracted" if raw_text else "empty",
                        "char_count": len(raw_text),
                    },
                })

    except (FileNotFoundError, ValueError):
        raise

    except Exception as exc:
        raise RuntimeError(
            f"Failed to extract PDF: {path}"
        ) from exc

    return documents

