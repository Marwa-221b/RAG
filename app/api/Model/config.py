
from pydantic import BaseModel
from typing import Optional

system_config = {
    "chunk_size": 200,
    "chunk_overlap": 20,
    "top_k": 5,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "temperature": 0.1,
    "max_length": 512,
    "vector_db_path": r"C:\Users\Sandra\OneDrive\Desktop\Third-year\NLP\Lab 8&9\RAG\data\vector_store",
    "data_directory": r"C:\Users\Sandra\OneDrive\Desktop\Third-year\NLP\Lab 8&9\RAG\data",
    "llm_model": "mock",
    "retrieval_strategy": "similarity"
}
class ConfigUpdate(BaseModel):
    chunk_size: Optional[int] = None
    chunk_overlap: Optional[int] = None
    top_k: Optional[int] = None
    embedding_model: Optional[str] = None
    temperature: Optional[float] = None
    llm_model: Optional[str] = None
    retrieval_strategy: Optional[str] = None
