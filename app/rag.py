from groq import Groq
from dotenv import load_dotenv
import os

from app.vector_store import search
from app.reranker import rerank_results


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. "
        "Add it to your .env file."
    )

client = Groq(
    api_key=GROQ_API_KEY
)


MODEL_NAME = "openai/gpt-oss-120b"


def answer_question(
    question: str,
    conversation: str = "",
    top_k: int = 10
):
    results = search(
        question,
        top_k=top_k
    )

    if not results:
        return {
            "answer": (
                "I don't have enough information "
                "in the provided document."
            ),
            "sources": []
        }

    results = rerank_results(
        question,
        results,
        top_k=5
    )

    if not results:
        return {
            "answer": (
                "I don't have enough information "
                "in the provided document."
            ),
            "sources": []
        }

    print(
        f"Best reranker score: "
        f"{results[0]['rerank_score']:.4f}"
    )

    context_parts = []

    for i, result in enumerate(
        results,
        start=1
    ):
        context_parts.append(
            f"""
[DOCUMENT CHUNK {i}]
Source: {result['source']}
Page: {result['page']}

{result['text']}
"""
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    if conversation.strip():
        conversation_section = f"""
PREVIOUS CONVERSATION:

{conversation}
"""
    else:
        conversation_section = """
PREVIOUS CONVERSATION:

No previous conversation.
"""

    prompt = f"""
You are an Enterprise AI Knowledge Copilot.

Your job is to answer questions about the
user's uploaded PDF.

The uploaded document is the ONLY source
of factual information.

IMPORTANT RULES:

1. Use ONLY the document context below
   for factual information.
2. Do not use outside knowledge.
3. Do not guess.
4. Do not invent information.
5. If the document contains enough information,
   answer the question clearly.
6. If the document does NOT contain enough
   information, say exactly:

"I don't have enough information in the provided document."

7. You may use previous conversation ONLY
   to understand follow-up questions.
8. Keep the answer concise and easy to understand.
9. Add page citations after factual claims.
10. Use this format:

[Page X]

11. Only cite pages that actually support
    the answer.
12. Never invent page numbers.

{conversation_section}

DOCUMENT CONTEXT:

{context}

CURRENT USER QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    answer = response.choices[0].message.content

    sources = []

    for result in results:
        sources.append({
            "source": result["source"],
            "page": result["page"],
            "score": result["rerank_score"],
            "faiss_score": result["faiss_score"],
            "bm25_score": result["bm25_score"]
        })

    return {
        "answer": answer,
        "sources": sources
    }