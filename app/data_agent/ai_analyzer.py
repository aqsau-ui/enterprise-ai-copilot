import json
import os

import pandas as pd
from dotenv import load_dotenv
from groq import Groq

from app.data_agent.analyzer import load_csv

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


def analyze_csv(
    file_path: str,
    question: str
):
    """
    Analyze a CSV dataset and answer a user's question.
    """

    dataframe = load_csv(file_path)

    dataset_preview = dataframe.head(10).to_dict(
        orient="records"
    )

    dataset_info = {
        "rows": len(dataframe),
        "columns": dataframe.columns.tolist(),
        "data_types": dataframe.dtypes.astype(str).to_dict(),
        "missing_values": dataframe.isnull()
        .sum()
        .to_dict(),
    }

    prompt = f"""
You are a Data Analyst AI.

The user has uploaded a CSV dataset.

Your job is to understand the dataset and
determine what analysis is needed to answer
the user's question.

DATASET INFORMATION:

{json.dumps(dataset_info, indent=2)}

SAMPLE DATA:

{json.dumps(dataset_preview, indent=2, default=str)}

USER QUESTION:

{question}

Return your response as JSON with exactly these fields:

{{
    "analysis_type": "description of the analysis needed",
    "answer": "your answer based only on the provided data"
}}

IMPORTANT:

1. Use only the provided dataset.
2. Do not invent values.
3. Do not use outside information.
4. If the question cannot be answered from
   the dataset, say so.
5. Keep the answer concise.
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
        max_tokens=500
    )

    answer = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer,
        "rows": len(dataframe),
        "columns": dataframe.columns.tolist()
    }