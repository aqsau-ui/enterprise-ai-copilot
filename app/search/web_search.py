import os

from dotenv import load_dotenv
from tavily import TavilyClient


# Load variables from .env
load_dotenv()


TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is missing. "
        "Add it to your .env file."
    )


client = TavilyClient(
    api_key=TAVILY_API_KEY
)


def web_search(
    query: str,
    max_results: int = 3
):
    """
    Search the web using Tavily.

    Returns a list of search results containing:
    - title
    - URL
    - content
    - relevance score
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=max_results,
        include_answer=False
    )

    results = []

    for result in response.get("results", []):

        results.append({
            "title": result.get(
                "title",
                ""
            ),
            "url": result.get(
                "url",
                ""
            ),
            "content": result.get(
                "content",
                ""
            )[:1200],
            "score": result.get(
                "score",
                0.0
            )
        })

    return results