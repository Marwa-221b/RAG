from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from ..Model.auth import UserCreate, UserLogin, Token, TokenData

router = APIRouter()

@router.get("/health/live")
async def liveness_check():
    """Liveness probe - checks if service is alive"""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat()
    }