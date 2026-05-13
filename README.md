# Multilingual RAG System (Arabic + English)

A scalable **Retrieval-Augmented Generation (RAG)** system designed for **Arabic and multilingual document understanding**.
The system processes raw unstructured documents such as PDFs, DOCX, and HTML files, then enables intelligent semantic search and grounded question answering using modern LLMs.


---

# 📌 Research Problem

Modern HR and recruitment systems generate massive amounts of unstructured multilingual data including:

* CVs in PDF and DOCX formats
* Job descriptions from websites
* Internal hiring documents
* Arabic and English mixed-content files

Recruiters often need to manually inspect every file to answer questions like:

* *Which candidates have Python experience?*
* *What certifications are required for this role?*
* *Who matches a cybersecurity position?*

This project solves the problem using a complete **end-to-end multilingual RAG pipeline** that:

1. Ingests raw messy documents
2. Cleans and preprocesses multilingual text
3. Chunks and embeds documents
4. Stores embeddings in a vector database
5. Retrieves relevant context
6. Generates grounded responses using LLMs

---

# ✨ Key Features

* Arabic text preprocessing

  * Diacritics removal
  * Arabic normalization
  * RTL text handling
* Multi-format document ingestion

  * PDF
  * DOCX
  * HTML
* Advanced retrieval system with embeddings
* FAISS vector database integration
* Modular LLM Factory architecture
* FastAPI backend
* Dockerized deployment
* Evaluation & benchmarking framework
* Cross-lingual Arabic ↔ English querying

---

# 🏗️ System Architecture

## Pipeline Flow

```text
Data Ingestion
      ↓
Arabic & Multilingual Preprocessing
      ↓
Chunking & Embedding
      ↓
Vector Storage (FAISS)
      ↓
Semantic Retrieval
      ↓
Context Assembly
      ↓
LLM Response Generation
      ↓
Evaluation & Monitoring
```

---


# 🌍 Arabic & Multilingual Support

## RTL Text Processing

Arabic PDF extraction often suffers from visual-order text corruption.
To solve this, the system uses:

* `arabic-reshaper`
* `python-bidi`

This converts extracted Arabic text into a logical order suitable for embeddings and LLM understanding.

---

## Arabic Normalization

Custom preprocessing logic normalizes:

* `أ`, `إ`, `آ` → `ا`
* `ة` → `ه`

This improves retrieval accuracy significantly.

---

## Diacritics Removal

Arabic diacritics (Tashkeel) are removed to ensure consistent semantic matching.

---

# 📥 Data Ingestion Pipeline

## Supported Formats

* PDF → `pdfplumber`
* DOCX → `python-docx`
* HTML → `BeautifulSoup4`

The ingestion system is designed to process **real messy documents** without manual cleaning.

---

# 🔍 Retrieval & Embedding System

## Embedding Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

### Vector Space

* 384-dimensional embeddings
* Semantic similarity search
* FAISS vector database

---

## Similarity Metric

The system uses **Cosine Similarity** instead of Euclidean distance.

This ensures retrieval focuses on:

* semantic meaning
* conceptual overlap
* skill alignment

rather than document length.

---

# ✂️ Strategic Chunking

## Chunk Size

```text
200 words
```

Chosen to balance:

* semantic completeness
* token efficiency
* retrieval quality

---

## Chunk Overlap

```text
20 words
```

Maintains semantic continuity between chunks and prevents boundary information loss.

---

# 🤖 RAG Engine & LLM Factory

## Features

* Modular provider-agnostic architecture
* Supports:

  * OpenAI
  * Gemini
  * Ollama
* Local LLM execution using Ollama
* Prompt templates for Arabic and English
* Keyword-aware reranking
* Context trimming for token optimization

---

# ⚙️ FastAPI Backend

The backend exposes REST APIs for:

* Authentication
* Configuration
* Document ingestion
* Query answering
* Monitoring

---

# 📘 API Documentation

## Base URL

```text
http://localhost:8000
```

## Authentication

JWT Bearer Token authentication is required for:

* `/config`
* `/ingest`
* `/query`

---

# 🔐 Authentication Endpoints

## Register User

### `POST /auth/register`

```json
{
  "username": "user",
  "email": "user@example.com",
  "password": "password"
}
```

---

## Login

### `POST /auth/login`

Returns JWT access token.

```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

---

# ⚙️ Configuration Endpoints

## Get Current Config

### `GET /config`

Returns:

* chunk size
* overlap
* top_k
* embedding model
* LLM model
* retrieval strategy

---

## Update Config

### `PUT /config`

Allows partial updates to:

* chunking settings
* retrieval strategy
* temperature
* embedding model

---

# ❤️ Health & Monitoring

## Liveness Probe

### `GET /health/live`

---

## Metrics

### `GET /metrics`

Returns:

* service status
* timestamps
* metadata

---

# 📄 Document Ingestion

## `POST /ingest`

Processes files from a folder and updates the vector store.

```json
{
  "folder_path": "/data/documents"
}
```

---

# 💬 Query Endpoint

## `POST /query`

Send natural language questions.

```json
{
  "query": "Which candidates have Python experience?"
}
```

### Response

```json
{
  "answer": "string",
  "sources": [
    {
      "chunk": "string",
      "source": "string"
    }
  ]
}
```

---

# 📊 Evaluation & Error Analysis

## System Performance

| Metric              | Value  |
| ------------------- | ------ |
| Total Queries       | 10     |
| Pass Rate           | 80%    |
| Retrieval Precision | 70%    |
| Factual Accuracy    | 60%    |
| Hallucination Rate  | 10%    |
| Mean Latency        | 26.94s |

---

# ⚠️ Failure Cases Identified

## Cross-Document Aggregation Failure

Problem:

* Retriever returns chunks from only one document

Proposed Fix:

* Metadata filtering
* Increase `top_k`

---

## Ambiguous Query Failure

Problem:

* Vague queries retrieve unrelated chunks

Proposed Fix:

* Query refinement layer
* Minimum specificity rules

---

## Cross-Lingual Retrieval Failure

Problem:

* English embeddings failed with Arabic queries

Proposed Fix:

* Switch to:

```text
paraphrase-multilingual-MiniLM-L12-v2
```

---

# 🐳 Docker Deployment

## Clone Repository

```bash
git clone https://github.com/Marwa-221b/RAG.git
cd rag-system
```

---

## Configure Environment


Edit `.env` with your settings.

---

## Start Services

```bash
docker-compose up --build
```

---

# 🌐 Access Services

| Service      | URL                                                      |
| ------------ | -------------------------------------------------------- |
| FastAPI      | [http://localhost:8000](http://localhost:8000)           |
| Swagger Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| GUI          | [http://localhost:8501](http://localhost:8501)           |

---

# 🧪 Tech Stack

* Python 3.11
* FastAPI
* FAISS
* HuggingFace Transformers
* OpenAI API
* Ollama
* Docker
* Docker Compose
* Pytest

---


# 🚀 Future Improvements

* Hybrid Retrieval (BM25 + Vector Search)
* Better multilingual embeddings
* Metadata-aware filtering
* Query expansion
* Advanced reranking models
* Streaming responses
* Kubernetes deployment

---

# 📌 Environment Variables

| Variable                    | Description           |
| --------------------------- | --------------------- |
| SECRET_KEY                  | JWT secret key        |
| ALGORITHM                   | JWT algorithm         |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time |

---

# 📜 License

This project is for educational .
