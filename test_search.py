from app.vector_store import search


results = search(
    "How can Docker containers be deployed?",
    top_k=3
)

print("\n===== SEARCH RESULTS =====\n")

for result in results:
    print(f"Page: {result['page']}")
    print(f"Source: {result['source']}")
    print(f"Score: {result['score']:.3f}")
    print(f"Text: {result['text'][:500]}")
    print("-" * 60)