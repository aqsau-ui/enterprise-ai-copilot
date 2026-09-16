import json
import re
import os

import pandas as pd
from dotenv import load_dotenv
from groq import Groq

from app.data_agent.analyzer import load_csv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# CREATE AI ANALYSIS PLAN
# ============================================================

def create_analysis_plan(
    question: str,
    dataframe: pd.DataFrame
) -> dict:

    columns = dataframe.columns.tolist()

    prompt = f"""
You are a data analysis planning agent.

The user has uploaded a CSV dataset.

Available columns:

{columns}

User question:

{question}

Your job is to create a JSON analysis plan.

Allowed operations:

1. count
2. average
3. highest
4. lowest
5. sum
6. columns
7. missing
8. preview
9. group_count
10. group_average
11. filter
12. relationship

============================================================
OPERATION RULES
============================================================

COUNT

Use when the user asks:

- how many customers
- number of customers
- total customers
- count of customers

Example:

"How many customers are there?"

JSON:

{{
    "operation": "count"
}}


============================================================
AVERAGE

Use when the user asks for an average of a numeric column.

Example:

"What is the average monthly fee?"

JSON:

{{
    "operation": "average",
    "column": "monthly_fee"
}}


============================================================
HIGHEST

Use when the user asks for the highest / maximum value.

Example:

"Which customer has the highest monthly fee?"

JSON:

{{
    "operation": "highest",
    "column": "monthly_fee"
}}


============================================================
LOWEST

Use when the user asks for the lowest / minimum value.

Example:

"Which customer has the lowest monthly fee?"

JSON:

{{
    "operation": "lowest",
    "column": "monthly_fee"
}}


============================================================
SUM

Use when the user asks for a total numeric value.

Example:

"What is the total monthly fee?"

JSON:

{{
    "operation": "sum",
    "column": "monthly_fee"
}}


============================================================
COLUMNS

Use when the user asks about available columns.

Example:

"What columns are in the dataset?"

JSON:

{{
    "operation": "columns"
}}


============================================================
MISSING

Use when the user asks about missing/null values.

Example:

"Which columns have missing values?"

JSON:

{{
    "operation": "missing"
}}


============================================================
PREVIEW

Use when the user asks to see sample rows.

Example:

"Show me the first few customers."

JSON:

{{
    "operation": "preview"
}}


============================================================
GROUP_COUNT

Use when the user wants counts broken down by a categorical column.

Examples:

"How many customers are in each plan?"

"How many customers are in each region?"

"How many customers use each payment method?"

JSON:

{{
    "operation": "group_count",
    "group_by": "plan"
}}


============================================================
GROUP_AVERAGE

Use when the user wants an average numeric value broken down by a category.

Examples:

"What is the average monthly fee by plan?"

"What is the average satisfaction score by region?"

"What is the average tenure by churn status?"

JSON:

{{
    "operation": "group_average",
    "column": "monthly_fee",
    "group_by": "plan"
}}


============================================================
FILTER

Use when the user asks to show only rows matching a condition.

Example:

"Show customers from the East region."

JSON:

{{
    "operation": "filter",
    "filter_column": "region",
    "filter_value": "East"
}}


============================================================
RELATIONSHIP
============================================================

IMPORTANT.

Use relationship ONLY when the user asks to:

- show the relationship between two numeric columns
- compare two numeric variables
- show X vs Y
- visualize X against Y
- show correlation-like relationship
- plot one numeric variable against another

Examples:

"Show the relationship between support tickets and satisfaction score."

"Show monthly fee vs tenure."

"Plot complaints against satisfaction score."

JSON:

{{
    "operation": "relationship",
    "x_column": "support_tickets",
    "y_column": "satisfaction_score"
}}

Do NOT convert relationship questions into group_average.

============================================================
VISUALIZATION TYPE
============================================================

Also decide whether the result should have a visualization.

Allowed visualization types:

- pie
- bar
- scatter
- none

Use PIE when the user asks about:

- proportion
- percentage
- share
- distribution
- composition

Examples:

"What percentage of customers use each payment method?"

"What is the proportion of churned vs non-churned customers?"

For these questions use group_count + pie.

Example:

{{
    "operation": "group_count",
    "group_by": "payment_method",
    "visualization": "pie"
}}


Use BAR when comparing categories.

Examples:

"Average monthly fee by plan."

"How many customers are in each region?"

"Average satisfaction by plan."

For these use group_average or group_count + bar.

Example:

{{
    "operation": "group_average",
    "column": "monthly_fee",
    "group_by": "plan",
    "visualization": "bar"
}}


Use SCATTER ONLY for relationships between TWO NUMERIC columns.

Example:

"Show the relationship between support tickets and satisfaction score."

JSON:

{{
    "operation": "relationship",
    "x_column": "support_tickets",
    "y_column": "satisfaction_score",
    "visualization": "scatter"
}}


For simple calculations use:

"visualization": "none"


============================================================
IMPORTANT
============================================================

Never invent column names.

Only use columns from:

{columns}

Return ONLY valid JSON.

Do not include markdown.

Do not include explanations.

The JSON must contain:

- operation
- visualization

Use null for fields that are not needed.

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
        max_tokens=300
    )

    content = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    # Remove markdown fences if the model adds them
    content = re.sub(
        r"```json\s*|\s*```",
        "",
        content
    ).strip()

    try:
        plan = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError(
            "The AI returned an invalid analysis plan."
        )

    return plan


# ============================================================
# VALIDATE COLUMN
# ============================================================

def validate_column(
    dataframe: pd.DataFrame,
    column: str
):

    if not column:
        raise ValueError(
            "No column was provided."
        )

    if column not in dataframe.columns:
        raise ValueError(
            f"Column '{column}' does not exist in the dataset."
        )


# ============================================================
# EXECUTE ANALYSIS
# ============================================================

def execute_analysis(
    dataframe: pd.DataFrame,
    plan: dict
) -> str:

    operation = plan.get("operation")

    column = plan.get("column")

    group_by = plan.get("group_by")

    filter_column = plan.get(
        "filter_column"
    )

    filter_value = plan.get(
        "filter_value"
    )

    x_column = plan.get(
        "x_column"
    )

    y_column = plan.get(
        "y_column"
    )


    # ========================================================
    # COUNT
    # ========================================================

    if operation == "count":

        return (
            f"Total customers: "
            f"{len(dataframe):,}"
        )


    # ========================================================
    # COLUMNS
    # ========================================================

    if operation == "columns":

        return (
            "Columns: "
            + ", ".join(dataframe.columns.tolist())
        )


    # ========================================================
    # PREVIEW
    # ========================================================

    if operation == "preview":

        return dataframe.head(5).to_string(
            index=False
        )


    # ========================================================
    # MISSING
    # ========================================================

    if operation == "missing":

        missing = (
            dataframe
            .isnull()
            .sum()
        )

        lines = [
            f"{column_name}: {count}"
            for column_name, count
            in missing.items()
        ]

        return (
            "Missing values:\n"
            + "\n".join(lines)
        )


    # ========================================================
    # AVERAGE
    # ========================================================

    if operation == "average":

        validate_column(
            dataframe,
            column
        )

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            raise ValueError(
                f"Column '{column}' is not numeric."
            )

        value = dataframe[column].mean()

        return (
            f"Average {column}: "
            f"{value:,.2f}"
        )


    # ========================================================
    # HIGHEST
    # ========================================================

    if operation == "highest":

        validate_column(
            dataframe,
            column
        )

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            raise ValueError(
                f"Column '{column}' is not numeric."
            )

        index = dataframe[column].idxmax()

        value = dataframe.loc[
            index,
            column
        ]

        return (
            f"Highest {column}: "
            f"{value:,.2f}"
        )


    # ========================================================
    # LOWEST
    # ========================================================

    if operation == "lowest":

        validate_column(
            dataframe,
            column
        )

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            raise ValueError(
                f"Column '{column}' is not numeric."
            )

        index = dataframe[column].idxmin()

        value = dataframe.loc[
            index,
            column
        ]

        return (
            f"Lowest {column}: "
            f"{value:,.2f}"
        )


    # ========================================================
    # SUM
    # ========================================================

    if operation == "sum":

        validate_column(
            dataframe,
            column
        )

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            raise ValueError(
                f"Column '{column}' is not numeric."
            )

        value = dataframe[column].sum()

        return (
            f"Total {column}: "
            f"{value:,.2f}"
        )


    # ========================================================
    # GROUP COUNT
    # ========================================================

    if operation == "group_count":

        validate_column(
            dataframe,
            group_by
        )

        grouped = (
            dataframe
            .groupby(
                group_by,
                dropna=False
            )
            .size()
        )

        lines = []

        for category, count in grouped.items():

            label = (
                "Missing"
                if pd.isna(category)
                else str(category)
            )

            lines.append(
                f"{label}: {count}"
            )

        return (
            f"Count by {group_by}:\n"
            + "\n".join(lines)
        )


    # ========================================================
    # GROUP AVERAGE
    # ========================================================

    if operation == "group_average":

        validate_column(
            dataframe,
            column
        )

        validate_column(
            dataframe,
            group_by
        )

        if not pd.api.types.is_numeric_dtype(
            dataframe[column]
        ):
            raise ValueError(
                f"Column '{column}' is not numeric."
            )

        grouped = (
            dataframe
            .groupby(
                group_by,
                dropna=False
            )[column]
            .mean()
        )

        lines = []

        for category, value in grouped.items():

            label = (
                "Missing"
                if pd.isna(category)
                else str(category)
            )

            lines.append(
                f"{label}: {value:,.2f}"
            )

        return (
            f"Average {column} by {group_by}:\n"
            + "\n".join(lines)
        )


    # ========================================================
    # FILTER
    # ========================================================

    if operation == "filter":

        validate_column(
            dataframe,
            filter_column
        )

        filtered = dataframe[
            dataframe[
                filter_column
            ]
            .astype(str)
            .str.lower()
            ==
            str(filter_value).lower()
        ]

        if filtered.empty:

            return (
                f"No rows found where "
                f"{filter_column} = "
                f"{filter_value}"
            )

        return (
            filtered
            .to_string(index=False)
        )


    # ========================================================
    # RELATIONSHIP
    # ========================================================

    if operation == "relationship":

        validate_column(
            dataframe,
            x_column
        )

        validate_column(
            dataframe,
            y_column
        )

        if not pd.api.types.is_numeric_dtype(
            dataframe[x_column]
        ):
            raise ValueError(
                f"Column '{x_column}' is not numeric."
            )

        if not pd.api.types.is_numeric_dtype(
            dataframe[y_column]
        ):
            raise ValueError(
                f"Column '{y_column}' is not numeric."
            )

        valid_rows = dataframe[
            [x_column, y_column]
        ].dropna()

        correlation = (
            valid_rows[x_column]
            .corr(
                valid_rows[y_column]
            )
        )

        return (
            f"Relationship between "
            f"{x_column} and {y_column}.\n"
            f"Correlation: {correlation:.2f}\n"
            f"Data points: {len(valid_rows)}"
        )


    raise ValueError(
        f"Unsupported analysis operation: "
        f"{operation}"
    )


# ============================================================
# BUILD VISUALIZATION DATA
# ============================================================

def build_visualization(
    dataframe: pd.DataFrame,
    plan: dict
):

    operation = plan.get("operation")

    visualization = plan.get(
        "visualization",
        "none"
    )


    # ========================================================
    # NO VISUALIZATION
    # ========================================================

    if visualization == "none":
        return None


    # ========================================================
    # PIE CHART
    # ========================================================

    if visualization == "pie":

        if operation != "group_count":
            return None

        group_by = plan.get(
            "group_by"
        )

        validate_column(
            dataframe,
            group_by
        )

        grouped = (
            dataframe
            .groupby(
                group_by,
                dropna=False
            )
            .size()
            .reset_index(
                name="value"
            )
        )

        chart_data = []

        for _, row in grouped.iterrows():

            label = row[group_by]

            if pd.isna(label):
                label = "Missing"

            chart_data.append(
                {
                    "label": str(label),
                    "value": int(
                        row["value"]
                    )
                }
            )

        return {
            "type": "pie",
            "title": (
                f"Distribution by "
                f"{group_by}"
            ),
            "xKey": "label",
            "yKey": "value",
            "xLabel": group_by,
            "yLabel": "Count",
            "data": chart_data
        }


    # ========================================================
    # BAR CHART
    # ========================================================

    if visualization == "bar":

        # --------------------------------------------
        # GROUP COUNT
        # --------------------------------------------

        if operation == "group_count":

            group_by = plan.get(
                "group_by"
            )

            validate_column(
                dataframe,
                group_by
            )

            grouped = (
                dataframe
                .groupby(
                    group_by,
                    dropna=False
                )
                .size()
                .reset_index(
                    name="value"
                )
            )

            chart_data = []

            for _, row in grouped.iterrows():

                label = row[group_by]

                if pd.isna(label):
                    label = "Missing"

                chart_data.append(
                    {
                        "label": str(label),
                        "value": int(
                            row["value"]
                        )
                    }
                )

            return {
                "type": "bar",
                "title": (
                    f"Count by "
                    f"{group_by}"
                ),
                "xKey": "label",
                "yKey": "value",
                "xLabel": group_by,
                "yLabel": "Count",
                "data": chart_data
            }


        # --------------------------------------------
        # GROUP AVERAGE
        # --------------------------------------------

        if operation == "group_average":

            column = plan.get(
                "column"
            )

            group_by = plan.get(
                "group_by"
            )

            validate_column(
                dataframe,
                column
            )

            validate_column(
                dataframe,
                group_by
            )

            grouped = (
                dataframe
                .groupby(
                    group_by,
                    dropna=False
                )[column]
                .mean()
                .reset_index()
            )

            chart_data = []

            for _, row in grouped.iterrows():

                label = row[group_by]

                if pd.isna(label):
                    label = "Missing"

                chart_data.append(
                    {
                        "label": str(label),
                        "value": round(
                            float(
                                row[column]
                            ),
                            2
                        )
                    }
                )

            return {
                "type": "bar",
                "title": (
                    f"Average "
                    f"{column} by "
                    f"{group_by}"
                ),
                "xKey": "label",
                "yKey": "value",
                "xLabel": group_by,
                "yLabel": (
                    f"Average {column}"
                ),
                "data": chart_data
            }


    # ========================================================
    # SCATTER CHART
    # ========================================================

    if visualization == "scatter":

        if operation != "relationship":
            return None

        x_column = plan.get(
            "x_column"
        )

        y_column = plan.get(
            "y_column"
        )

        validate_column(
            dataframe,
            x_column
        )

        validate_column(
            dataframe,
            y_column
        )

        if not pd.api.types.is_numeric_dtype(
            dataframe[x_column]
        ):
            raise ValueError(
                f"Column '{x_column}' is not numeric."
            )

        if not pd.api.types.is_numeric_dtype(
            dataframe[y_column]
        ):
            raise ValueError(
                f"Column '{y_column}' is not numeric."
            )

        valid_rows = dataframe[
            [x_column, y_column]
        ].dropna()

        chart_data = []

        for _, row in valid_rows.iterrows():

            chart_data.append(
                {
                    "x": float(
                        row[x_column]
                    ),
                    "y": float(
                        row[y_column]
                    )
                }
            )

        return {
            "type": "scatter",
            "title": (
                f"{x_column} vs "
                f"{y_column}"
            ),
            "xKey": "x",
            "yKey": "y",
            "xLabel": x_column,
            "yLabel": y_column,
            "data": chart_data
        }


    return None


# ============================================================
# MAIN AGENT
# ============================================================

def analyze_with_agent(
    file_path: str,
    question: str
) -> dict:

    # Load CSV
    dataframe = load_csv(
        file_path
    )

    # Ask AI to create plan
    plan = create_analysis_plan(
        question,
        dataframe
    )

    print(
        "Analysis plan:",
        plan
    )

    # Execute deterministic analysis
    result = execute_analysis(
        dataframe,
        plan
    )

    # Build visualization
    visualization = build_visualization(
        dataframe,
        plan
    )

    return {
        "question": question,

        "plan": plan,

        "result": result,

        "visualization":
            visualization,

        "rows": len(
            dataframe
        ),

        "columns":
            dataframe.columns.tolist()
    }