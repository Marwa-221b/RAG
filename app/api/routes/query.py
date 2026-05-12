from fastapi import APIRouter, Depends
from pydantic import BaseModel

from rag.context_builder import get_context_from_query
from .auth import get_current_user
from dotenv import load_dotenv
from rag.generator import generate_answer

from ..Model.config import system_config as config
# =======
# from core.config import get_llm_config  
# >>>>>>> origin/main

load_dotenv()
router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    

@router.post("/query")
async def query_endpoint(request: QueryRequest, current_user: dict = Depends(get_current_user)):
   result=get_context_from_query(request.query)
   answer = generate_answer(request.query, result["sources"], config)
   return {
       "answer": answer,
        "sources": result.get("sources", [])
   }