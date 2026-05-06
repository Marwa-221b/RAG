from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from ..Model.auth import UserCreate, UserLogin, Token, TokenData

router = APIRouter()

@router.get("/metrics")
async def eval_mit():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "RAG API",
    }