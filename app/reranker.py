from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(MODEL_NAME)


def rerank_results(
    query: str,
    results: list[dict],
    top_k: int = 5
) -> list[dict]:

    if not results:
        return []

    pairs = []

    for result in results:

        text = (
            result.get("text")
            or result.get("content")
            or ""
        )

        pairs.append(
            (query, text)
        )

    scores = reranker.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):

        item = result.copy()

        item["rerank_score"] = float(score)

        reranked.append(item)

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked[:top_k]