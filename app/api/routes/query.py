from fastapi import APIRouter, Depends
from opentelemetry import context
from pydantic import BaseModel
from .auth import get_current_user
from rag.context_builder import get_context_from_query

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def query_endpoint(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    result=get_context_from_query(request.query)
    return {"answer": f"You asked: {result['query']}" , "sources": result["sources"],"context":result["context"]}