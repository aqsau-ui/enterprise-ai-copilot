from groq import Groq
from dotenv import load_dotenv
import os
import re

from app.search.web_search import web_search


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


def answer_web_question(
    question: str,
    top_k: int = 3
):
    """
    Answer a general question using web search
    and Groq.
    """

    results = web_search(
        query=question,
        max_results=top_k
    )

    if not results:
        return {
            "answer": "I couldn't find enough information on the web.",
            "sources": []
        }

    context_parts = []

    for i, result in enumerate(results, start=1):

        context_parts.append(
            f"""
[WEB SOURCE {i}]

Title:
{result['title']}

URL:
{result['url']}

Content:
{result['content']}
"""
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are an AI web research assistant.

Answer the user's question using ONLY the
web sources provided below.

RULES:

1. Use only the provided web sources.
2. Do not use outside knowledge.
3. Do not invent facts.
4. If the sources do not contain enough
   information, say so clearly.
5. Keep the answer concise and useful.
6. Answer the user's question directly.
7. Keep the answer concise and useful.
8. Usually use 1-3 short paragraphs or 3-6 bullet points.
9. Do not create a table unless the user specifically asks for a table or comparison.
10. Cite factual claims using [Source 1], [Source 2], or [Source 3].
11. Use ONLY this citation format: [Source N].
12. Never use citation formats such as 【1】, [1], or footnotes.
13. Do not mention information that is not supported by the provided sources.
14. Do not repeat the source content unnecessarily.
15. If the sources do not provide enough information, say so clearly.

WEB SOURCES:

{context}

USER QUESTION:

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
        temperature=0.1,
        max_tokens=700
    )

    answer = response.choices[0].message.content
    answer = re.sub(
    r"【(\d+)】",
    r"[Source \1]",
    answer
)

    sources = []

    for result in results:
        sources.append({
            "title": result["title"],
            "url": result["url"],
            "score": result.get("score", 0.0)
        })

    return {
        "answer": answer,
        "sources": sources
    }