import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .pdf_loader import load_pdf
from .text_normalizer import normalize_documents
from .chunker import chunk_documents
from .embedding import embed_documents
from .vector_store import add_chunks
from .retriever import retrieve_context



load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = BASE_DIR / "data" / "pdfs"


LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL")
LLM_MODEL = os.getenv("LLM_MODEL")


def get_llm_client() -> OpenAI:

    if not LLM_API_KEY:
        raise ValueError("LLM_API_KEY is not configured.")

    if not LLM_BASE_URL:
        raise ValueError("LLM_BASE_URL is not configured.")

    if not LLM_MODEL:
        raise ValueError("LLM_MODEL is not configured.")

    return OpenAI(
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL
    )


def ingest_documents() -> None:

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {PDF_DIR}"
        )

    all_documents = []

    for pdf_file in pdf_files:

        print(f"Loading: {pdf_file.name}")

        documents = load_pdf(pdf_file)
        all_documents.extend(documents)

    print(f"Loaded {len(all_documents)} pages.")

    
    normalized_documents = normalize_documents(
        all_documents
    )

    
    chunks = chunk_documents(
        normalized_documents
    )

    print(f"Generated {len(chunks)} chunks.")

    if not chunks:
        raise ValueError("No valid text chunks found.")

    
    embedded_chunks = embed_documents(chunks)

    print(f"Generated {len(embedded_chunks)} embeddings.")

    
    add_chunks(embedded_chunks)

    print("Documents successfully stored in ChromaDB.")


def generate_answer(question: str) -> dict:


    if not question.strip():
        raise ValueError("Question cannot be empty.")

    
    retrieval_result = retrieve_context(question)

    context = retrieval_result["context"]
    sources = retrieval_result["sources"]

    if not context:
        return {
            "answer": "اطلاعات مرتبطی در اسناد ذخیره‌شده پیدا نشد.",
            "sources": []
        }

    
    client = get_llm_client()

    system_prompt = """
    تو یک دستیار پرسش و پاسخ هستی که فقط بر اساس
    اطلاعات موجود در Context به سؤالات پاسخ می‌دهد.

    قوانین:
    1. پاسخ باید بر اساس اطلاعات Context باشد.
    2. اگر پاسخ سؤال در Context وجود ندارد،
       صریحاً اعلام کن که اطلاعات کافی در اسناد وجود ندارد.
    3. اطلاعات یا منابع جدید از خودت اضافه نکن.
    4. پاسخ‌ها را به زبان فارسی و واضح ارائه بده.
    """

    user_prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.2,
        max_tokens=2048
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError("LLM returned an empty response.")

    return {
        "answer": answer,
        "sources": sources
    }


def main() -> None:

    print("\n===== Persian RAG System =====")

    while True:

        print("\n1. Ingest PDF documents")
        print("2. Ask a question")
        print("3. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":

            try:
                ingest_documents()

            except Exception as exc:
                print(f"Ingestion failed: {exc}")

        elif choice == "2":

            question = input("\nEnter your question: ").strip()

            if not question:
                print("Question cannot be empty.")
                continue

            try:
                result = generate_answer(question)

                print("\n===== Answer =====")
                print(result["answer"])

                print("\n===== Sources =====")

                for source in result["sources"]:
                    print(
                        f"- {source['file_name']} "
                        f"(Page {source['page']})"
                    )

            except Exception as exc:
                print(f"Error: {exc}")

        elif choice == "3":

            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()