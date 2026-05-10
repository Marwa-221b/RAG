
from pydantic import BaseModel
from typing import Optional
import os

system_config = {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "top_k": 5,
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "temperature": 0.7,
    "max_length": 512,
    "vector_db_path": os.getenv("VECTOR_DB_PATH", "./data/vector_db"),
    "data_directory": os.getenv("DATA_DIRECTORY", "./data/orgin_doc"),
    "llm_model": "ollama",
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
