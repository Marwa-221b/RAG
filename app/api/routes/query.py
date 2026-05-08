from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .auth import get_current_user
import os
from dotenv import load_dotenv
from services.retrieval.integration_pip_ret import vector_store_from_pipline
from services.retrieval.retriever import retrieve
from rag.generator import generate_answer
from ..Model.config import system_config as config

load_dotenv()
router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    
vector_store = vector_store_from_pipline()


@router.post("/query")
async def query_endpoint(request: QueryRequest, current_user: dict = Depends(get_current_user)):
   docs = retrieve(request.query, vector_store)
   answer = generate_answer(request.query, docs, config)
   return {
       "answer": answer,
       "sources": docs
   }