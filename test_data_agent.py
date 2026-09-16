from app.data_agent.analyzer import (
    load_csv,
    get_dataset_info
)


file_path = "data/datasets/employees.csv"

df = load_csv(file_path)

print("\nDATASET:")
print(df)

print("\nDATASET INFO:")

info = get_dataset_info(df)

for key, value in info.items():
    print(f"{key}: {value}")