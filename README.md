# Enterprise AI Knowledge Copilot

An AI-powered workspace that combines **document question answering, web search, natural-language data analysis, and interactive data visualization** in one application.

The project demonstrates a production-oriented AI architecture using **Retrieval-Augmented Generation (RAG), hybrid retrieval, semantic reranking, LLM-based planning, deterministic data execution, and source-aware responses**.

---

## Overview

Enterprise information is often spread across documents, web resources, and structured datasets.

The **Enterprise AI Knowledge Copilot** provides a single interface for working with these different information sources.

Users can:

- Upload a PDF and ask questions about its contents
- Search the web for current information
- Upload CSV datasets and analyze them using natural language
- Generate visualizations from dataset analysis
- View sources and references supporting AI responses

The system separates different AI workflows into dedicated modes:

```text
Document AI
    ↓
PDF → Chunking → Embeddings → FAISS + BM25
    ↓
Hybrid Retrieval → Reranking → LLM
    ↓
Answer + Page Citations


Web Search Agent
    ↓
User Question
    ↓
Web Search → Relevant Sources
    ↓
LLM
    ↓
Answer + Source References


AI Data Analyst
    ↓
CSV Dataset
    ↓
Natural Language Question
    ↓
LLM Analysis Plan
    ↓
Deterministic Pandas Execution
    ↓
Result + Visualization
```

## Features

### 1. Document AI / RAG

Upload a PDF and ask questions about the document.

The system uses a Retrieval-Augmented Generation pipeline instead of sending the entire document directly to the LLM.

#### Pipeline

```text
PDF Upload
    ↓
PDF Text Extraction
    ↓
Text Chunking
    ↓
Sentence Transformer Embeddings
    ↓
FAISS Semantic Search
       +
BM25 Keyword Search
    ↓
Hybrid Retrieval
    ↓
Cross-Encoder Reranking
    ↓
Relevant Context
    ↓
Groq LLM
    ↓
Answer + Page Citations
```

#### Technologies

- PyPDF
- Sentence Transformers
- FAISS
- BM25
- Cross-Encoder
- Groq
- FastAPI

#### Example questions

- What is this document about?
- What experience does the candidate have?
- What technologies are mentioned?
- What interests the candidate about the company?
- What projects are described in the document?

The system is instructed to use the uploaded document as the factual source and to indicate when the document does not contain enough information.

### 2. Hybrid Retrieval

The document search system combines two retrieval approaches.

**Semantic Retrieval**

FAISS searches using vector embeddings.

This helps retrieve text that is conceptually similar to the user's question.

**Keyword Retrieval**

BM25 performs keyword-based retrieval.

This helps with exact terms, names, technologies, and other important keywords.

**Hybrid Retrieval**

The system combines both retrieval signals before reranking the candidate chunks.

```text
                 User Question
                       │
             ┌─────────┴─────────┐
             │                   │
             ▼                   ▼
       FAISS Search          BM25 Search
       Semantic              Keyword
             │                   │
             └─────────┬─────────┘
                       ▼
               Candidate Chunks
                       │
                       ▼
              Cross-Encoder
                Reranking
                       │
                       ▼
              Top Relevant Chunks
```

This provides both semantic and lexical retrieval signals.

### 3. Cross-Encoder Reranking

After hybrid retrieval, the retrieved chunks are passed through a cross-encoder reranker.

The reranker evaluates the relationship between:

```text
User Question
       +
Retrieved Document Chunk
```

The highest-scoring chunks are then provided to the LLM.

This creates a two-stage retrieval pipeline:

```text
Retrieval
   ↓
Candidate Documents
   ↓
Reranking
   ↓
Best Context
   ↓
LLM
```

### 4. Web Search Agent

The application also includes a separate web search workflow for questions that require information from the internet.

#### Pipeline

```text
User Question
      ↓
Tavily Web Search
      ↓
Search Results
      ↓
Relevant Source Content
      ↓
Groq LLM
      ↓
Concise Answer
      ↓
Source References
```

The web agent provides source references such as:

```text
[Source 1]
[Source 2]
[Source 3]
```

The application keeps the web-search workflow separate from document question answering.

#### Example questions

- What are the latest developments in AI?
- What are the current challenges in AI adoption?
- What are the latest trends in software engineering?
- What companies are currently hiring for AI roles?

### 5. AI Data Analyst

The application includes an AI-powered data analysis workflow for CSV datasets.

Instead of asking the LLM to directly calculate numerical answers, the LLM first converts the natural-language question into a structured analysis plan.

The application then executes that plan using Pandas.

#### Pipeline

```text
CSV Upload
    ↓
Pandas DataFrame
    ↓
User Question
    ↓
LLM Analysis Planning
    ↓
Structured Analysis Plan
    ↓
Validation
    ↓
Pandas Execution
    ↓
Result
```

#### Example

User:

> What is the average salary by department?

The LLM may produce a structured plan such as:

```json
{
  "operation": "group_average",
  "column": "salary",
  "group_by": "department"
}
```

Pandas then performs the actual calculation.

This separates:

```text
Language Understanding
        ↓
LLM

Numerical Computation
        ↓
Pandas
```

This design reduces the risk of the LLM inventing or incorrectly calculating numerical results.

#### Supported Data Analysis Operations

The Data Analyst currently supports:

- Average
- Sum
- Count
- Highest
- Lowest
- Grouped average
- Grouped count
- Filtering
- Missing-value analysis
- Dataset preview
- Column inspection

#### Example questions

- What is the average salary?
- What is the highest salary?
- What is the lowest salary?
- How many employees are there?
- What is the average salary by department?
- How many customers are in each plan?
- How many customers are in each region?
- What is the churn count by plan?
- What is the average monthly fee by churn status?
- Which columns have missing values?
- Show the first five rows.

### 6. Data Visualization

The Data Analyst can generate visualizations based on the actual dataset analysis.

Supported visualizations include:

- Bar charts
- Line charts
- Pie charts
- Grouped comparisons
- Missing-value charts
- KPI-style numerical results

For example:

> What is the average monthly fee by plan?

can produce a grouped comparison.

Another example:

> How many customers are in each plan?

can produce a category distribution.

Charts are generated from the dataset and analysis results rather than being invented by the LLM.

## Architecture

```text
                         ┌───────────────────────┐
                         │      React UI         │
                         │    TypeScript         │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌───────────────────────┐
                         │      FastAPI          │
                         │       Backend         │
                         └───────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
      ┌───────────────┐      ┌───────────────┐     ┌───────────────┐
      │  Document AI  │      │  Web Search    │     │ Data Analyst  │
      │     RAG       │      │     Agent      │     │     Agent     │
      └───────┬───────┘      └───────┬───────┘     └───────┬───────┘
              │                      │                      │
              ▼                      ▼                      ▼
        PDF Pipeline           Tavily Search           Pandas
              │                      │                      │
              ▼                      ▼                      ▼
       FAISS + BM25             Web Sources          CSV Dataset
              │                      │                      │
              ▼                      ▼                      ▼
        Cross-Encoder               Groq              Visualization
         Reranking                  LLM
              │
              ▼
             Groq
              LLM
```

## Technology Stack

### Backend

- Python
- FastAPI
- Uvicorn
- Pandas
- PyPDF

### AI / Machine Learning

- Sentence Transformers
- FAISS
- BM25
- Cross-Encoder
- Groq
- LLM-based analysis planning

### Web Search

- Tavily

### Frontend

- React
- TypeScript
- Vite
- Recharts

### Development

- Git
- GitHub
- Python virtual environment
- REST APIs

## Project Structure

```text
enterprise-ai-copilot/
│
├── app/
│   │
│   ├── data_agent/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── ai_analyzer.py
│   │   └── analyzer.py
│   │
│   ├── search/
│   │   ├── __init__.py
│   │   └── web_search.py
│   │
│   ├── chunker.py
│   ├── embeddings.py
│   ├── main.py
│   ├── pdf_processor.py
│   ├── rag.py
│   ├── reranker.py
│   ├── vector_store.py
│   └── web_agent.py
│
├── data/
│   └── datasets/
│       ├── employees.csv
│       ├── complex_employees.csv
│       ├── complex_ecommerce.csv
│       └── customer_churn.csv
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.ts
│
├── tests/
│
├── .gitignore
├── README.md
├── requirements.txt
├── test_ai_analyzer.py
├── test_data_agent.py
├── test_data_agent_ai.py
├── test_rag.py
└── test_search.py
```

## API Endpoints

The FastAPI backend exposes separate endpoints for the application's workflows.

### Health Check

```text
GET /health
```

Returns the API health status.

### Document Question Answering

```text
GET /ask
```

Parameters:

- `question`
- `conversation`

Example:

```text
GET /ask?question=What is this document about?
```

### PDF Upload

```text
POST /upload
```

Uploads a PDF and rebuilds the active vector store.

The current application uses the most recently uploaded document as the active document for document question answering.

### Web Search

```text
GET /web-search
```

Example:

```text
GET /web-search?query=latest AI trends
```

Returns search results from the web.

### Web AI Question Answering

```text
GET /web-ask
```

Example:

```text
GET /web-ask?query=What are the latest AI trends?
```

The search results are passed to the LLM to generate a concise answer.

### CSV Upload

```text
POST /data-upload
```

Uploads a CSV dataset.

Only CSV files are accepted.

### Data Analysis

```text
GET /data-ask
```

Parameters:

- `question`
- `filename`

Example:

```text
GET /data-ask?question=What is the average salary?&filename=employees.csv
```

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/aqsau-ui/enterprise-ai-copilot.git
```

Move into the project:

```bash
cd enterprise-ai-copilot
```

### Backend Setup

#### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\Activate.ps1
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit `.env` to GitHub.

The repository `.gitignore` excludes environment files and local generated data.

### Start the Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### Frontend Setup

Open a second terminal.

Move into the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

## Example Workflow

### Document AI

1. Open the application.
2. Select Document AI.
3. Upload a PDF.
4. Wait for processing to finish.
5. Ask a question about the document.
6. Review the answer and page citations.

### Web Search

1. Select Web Search.
2. Enter a question.
3. The application searches the web.
4. Retrieved sources are provided to the LLM.
5. The answer is returned with source references.

### Data Analyst

1. Select Data Analyst.
2. Upload a CSV file.
3. Ask a natural-language question.
4. The AI creates an analysis plan.
5. Pandas executes the operation.
6. The result is displayed.
7. A visualization may be generated when appropriate.
