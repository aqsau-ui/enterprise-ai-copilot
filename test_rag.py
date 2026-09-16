from app.rag import answer_question


result = answer_question(
    "What is the assignment about?"
)

print("\n===== AI ANSWER =====\n")
print(result["answer"])

print("\n===== SOURCES =====\n")

for source in result["sources"]:
    print(
        f"{source['source']} | "
        f"Page {source['page']} | "
        f"Score {source['score']:.3f}"
    )