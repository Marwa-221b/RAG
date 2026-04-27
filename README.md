# Multilingual RAG System (Arabic + English)

This project implements a scalable Retrieval-Augmented Generation (RAG) system with strong support for Arabic and multilingual data.

The system is designed using modular, independent workstreams to enable parallel development across a 6-member team.

## Key Features

- Arabic text preprocessing (diacritics removal, normalization, RTL handling)
- Document ingestion pipeline (PDF, DOCX, HTML)
- Advanced retrieval system with embeddings and vector database
- Modular LLM integration (OpenAI, Gemini, Ollama)
- FastAPI backend for serving queries
- Dockerized infrastructure with CI/CD
- Evaluation framework with retrieval and generation metrics

## Architecture Overview

Pipeline:
1. Data Ingestion & Preprocessing
2. Chunking & Embedding
3. Vector Storage & Retrieval
4. Context Assembly
5. LLM Response Generation
6. Evaluation & Monitoring

## Team Workstreams

Each module is designed to be developed independently:

- Data Pipeline & Arabic Support
- Retrieval Stack
- FastAPI Backend
- RAG Engine & LLM Factory
- Infrastructure & DevOps
- Evaluation & Testing

## Tech Stack

- Python
- FastAPI
- Vector DB (FAISS / Chroma / Pinecone)
- HuggingFace / OpenAI embeddings
- Docker & Docker Compose
- Pytest for testing

## Getting Started

```bash
git clone <repo>
cd rag-project
docker-compose up --build
