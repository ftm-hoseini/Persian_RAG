
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")
MODEL = os.getenv("LLM_MODEL", "edrac-2")


if not API_KEY:
    raise ValueError("LLM_API_KEY is not set in environment variables.")

if not BASE_URL:
    raise ValueError("LLM_BASE_URL is not set in environment variables.")


client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
    timeout=60.0,
)


def generate_answer(question: str, context: str) -> str:
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    if not context.strip():
        raise ValueError("Context cannot be empty.")

    system_prompt = """
    You are a question-answering assistant.

    Answer the user's question using only the provided context.

    Rules:
    - Do not use external knowledge.
    - If the context does not contain enough information,
      clearly state that the available documents do not provide
      sufficient information to answer the question.
    - Answer in Persian.
    - Be clear and concise.
    """

    user_prompt = f"""
    Context:
    {context}

    Question:
    {question}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        answer = response.choices[0].message.content

        if not answer:
            raise ValueError("LLM returned an empty response.")

        return answer.strip()

    except Exception as exc:
        raise RuntimeError("Failed to generate answer using LLM.") from exc

