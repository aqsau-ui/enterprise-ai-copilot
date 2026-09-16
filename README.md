# Enterprise AI Knowledge Copilot

An AI-powered workspace that lets users chat with documents, search the web, and analyze CSV datasets using natural language.

The project combines Retrieval-Augmented Generation (RAG), hybrid search, semantic reranking, web search, AI-powered data analysis, and interactive data visualization in one application.

---

## Features

### 1. Document AI

Upload a PDF and ask questions about its contents.

The document pipeline uses:

- PDF text extraction
- Text chunking
- Sentence Transformers
- FAISS vector search
- BM25 keyword search
- Hybrid retrieval
- Cross-encoder reranking
- Groq LLM generation
- Page-level citations

The system is designed to answer using the uploaded document rather than relying on outside knowledge.

---

### 2. Web Search Agent

Ask questions that require current information from the web.

The web agent:

1. Receives the user's question
2. Searches the web
3. Retrieves relevant sources
4. Passes the sources to the LLM
5. Generates a concise answer
6. Provides source references

Web search is powered by Tavily.

---

### 3. AI Data Analyst

Upload a CSV dataset and ask questions using natural language.

Examples:

```text
What is the average salary?

What is the average salary by department?

How many customers are in each plan?

What is the churn count by plan?

Which columns have missing values?

What is the average monthly fee by churn status?
The Data Analyst converts the natural-language question into a structured analysis plan.

The application then executes the requested operation deterministically using Pandas.

Supported operations include:

Average
Sum
Count
Highest
Lowest
Grouped average
Grouped count
Filtering
Missing-value analysis
Dataset preview
Column inspection
4. Data Visualization

The Data Analyst can generate visualizations from the actual dataset.

The application supports different chart types depending on the analysis.

Examples include:

Bar charts for category comparisons
Bar charts for grouped averages
Bar charts for grouped counts
Pie charts for distributions
Charts for missing-value analysis
KPI-style results for single numerical values

For example:

What is the average monthly fee by plan?

can produce a grouped comparison chart.

How many customers are in each plan?

can produce a category-count chart.

How many customers churned versus did not churn?

can produce a distribution visualization.

Charts are generated from the actual Pandas analysis results rather than invented by the LLM.

Architecture
                         ┌──────────────────────┐
                         │      React UI        │
                         │                      │
                         │ Document │ Web │ Data│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │ Document RAG │    │ Web Search   │    │ Data Analyst │
        └──────┬───────┘    └──────┬───────┘    └──────┬───────┘
               │                   │                   │
               ▼                   ▼                   ▼
        ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
        │ FAISS + BM25 │    │    Tavily    │    │    Pandas    │
        └──────┬───────┘    └──────────────┘    └──────┬───────┘
               │                                       │
               ▼                                       ▼
        ┌──────────────┐                       ┌──────────────┐
        │ CrossEncoder │                       │ Visualization│
        │  Reranking   │                       │    Charts    │
        └──────┬───────┘                       └──────────────┘
               │
               ▼
        ┌──────────────┐
        │   Groq LLM   │
        └──────────────┘
Document RAG Pipeline
PDF Upload
    │
    ▼
Text Extraction
    │
    ▼
Text Chunking
    │
    ▼
Sentence Transformer Embeddings
    │
    ▼
┌───────────────┬───────────────┐
│               │               │
▼               ▼               │
FAISS          BM25             │
Semantic       Keyword          │
Search         Search           │
│               │               │
└───────┬───────┘
        │
        ▼
Hybrid Retrieval
        │
        ▼
Cross-Encoder Reranking
        │
        ▼
Top Relevant Chunks
        │
        ▼
Groq LLM
        │
        ▼
Answer + Page Citations
Data Analyst Pipeline
CSV Upload
    │
    ▼
Pandas DataFrame
    │
    ▼
Natural Language Question
    │
    ▼
Groq LLM
    │
    ▼
Structured Analysis Plan
    │
    ▼
Plan Validation
    │
    ▼
Pandas Execution
    │
    ├──────────────► Numerical Result
    │
    └──────────────► Chart Data
                         │
                         ▼
                    React Chart

The LLM is responsible for understanding the user's question and creating an analysis plan.

Pandas performs the actual numerical calculation.

This separation helps reduce hallucinated numerical results.

Tech Stack
Backend
Python
FastAPI
Uvicorn
Pandas
PyPDF
FAISS
BM25
Sentence Transformers
Cross-Encoder
Groq
Tavily
Frontend
React
TypeScript
Vite
Recharts
CSS
AI / ML
Retrieval-Augmented Generation
Semantic Search
Keyword Search
Hybrid Retrieval
Cross-Encoder Reranking
Large Language Models
Natural Language Data Analysis