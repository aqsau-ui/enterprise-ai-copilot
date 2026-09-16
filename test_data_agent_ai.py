from app.data_agent.agent import analyze_with_agent


file_path = "data/datasets/employees.csv"


questions = [

    "What is the average salary?",

    "Who has the highest salary?",

    "Who has the lowest salary?",

    "How many employees are there?",

    "What columns are in the dataset?",

    "Are there any missing values?",

    "What is the average salary by department?",

    "What is the number of employees in each department?",

    "What is the total salary?",

    "Show me the employees in Engineering"

]


for question in questions:

    print("\n" + "=" * 70)

    print("QUESTION:")
    print(question)

    try:

        result = analyze_with_agent(
            file_path,
            question
        )

        print("\nAI PLAN:")
        print(result["plan"])

        print("\nACTUAL RESULT:")
        print(result["result"])

    except Exception as error:

        print("\nERROR:")
        print(error)