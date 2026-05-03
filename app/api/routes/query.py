from fastapi import APIRouter, Depends
from pydantic import BaseModel
from .auth import get_current_user

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def query_endpoint(request: QueryRequest, current_user: dict = Depends(get_current_user)):
    return {"answer": f"You asked: {request.query}", "sources": []}