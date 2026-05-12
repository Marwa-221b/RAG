from fastapi import APIRouter, Depends
from pydantic import BaseModel

from rag.context_builder import get_context_from_query
from .auth import get_current_user
import os
from dotenv import load_dotenv
from services.retrieval.integration_pip_ret import vector_store_from_pipline
from services.retrieval.retriever import retrieve
from rag.generator import generate_answer

from ..Model.config import system_config as config
# =======
# from core.config import get_llm_config  
# >>>>>>> origin/main

load_dotenv()
router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    

vector_store = vector_store_from_pipline()
# =======
# # vector_store = vector_store_from_pipline("data")
# >>>>>>> origin/main


@router.post("/query")
async def query_endpoint(request: QueryRequest, current_user: dict = Depends(get_current_user)):
   result=get_context_from_query(request.query)
   docs = retrieve(request.query, vector_store)
   formatted_sources = []
   for doc in docs:
        source_info = {
            "source": doc.get('metadata', {}).get('source', doc.get('source', 'unknown')),
            "doc_id": doc.get('doc_id', 'unknown'),
            "file_type": doc.get('metadata', {}).get('file_type', 'unknown'),
            "chunk_preview": doc.get('chunks', '')[:200] if doc.get('chunks') else ''
        }
        formatted_sources.append(source_info)
   answer = generate_answer(request.query, result["sources"], config)
   return {
       "answer": answer,
        "sources":  formatted_sources
   }