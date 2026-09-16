from app.data_agent.ai_analyzer import analyze_csv


file_path = "data/datasets/employees.csv"


questions = [
    "What is the average salary?",
    "Who has the highest salary?",
    "Who has the lowest salary?",
    "How many employees are there?",
    "What columns are in the dataset?",
    "Are there any missing values?"
]


for question in questions:

    print("\nQUESTION:")
    print(question)

    result = analyze_csv(
        file_path,
        question
    )

    print("ANSWER:")
    print(result["answer"])