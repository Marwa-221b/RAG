from ..Model.config import ConfigUpdate
from ..Model.config import system_config
from fastapi import APIRouter, Depends, HTTPException, status
from  .auth import get_current_user



router = APIRouter()


@router.get("/config")
async def get_config(current_user: dict = Depends(get_current_user)):
    """
    Get current system configuration.
    This endpoint is required for Member 3's tasks.
    """
    return {
        "config": system_config,
        "service": "RAG API",
        "version": "1.0.0"
    }

@router.put("/config")
async def update_config(
    updates: ConfigUpdate,
    current_user: dict = Depends(get_current_user)
):

    
    if updates.chunk_size is not None:
        system_config["chunk_size"] = updates.chunk_size
        
    
    if updates.chunk_overlap is not None:
        if updates.chunk_overlap >= system_config["chunk_size"]:
            raise HTTPException(
                status_code=400,
                detail="chunk_overlap must be less than chunk_size"
            )
        system_config["chunk_overlap"] = updates.chunk_overlap
    
    if updates.top_k is not None:
        system_config["top_k"] = updates.top_k
      
    
    if updates.embedding_model is not None:
        system_config["embedding_model"] = updates.embedding_model
       
    
    if updates.temperature is not None:
        if 0 <= updates.temperature <= 2:
            system_config["temperature"] = updates.temperature
        else:
            raise HTTPException(
                status_code=400,
                detail="temperature must be between 0 and 2"
            )
    
    if updates.llm_model is not None:
        system_config["llm_model"] = updates.llm_model
    
    if updates.retrieval_strategy is not None:
        valid_strategies = ["similarity", "mmr", "hybrid"]
        if updates.retrieval_strategy in valid_strategies:
            system_config["retrieval_strategy"] = updates.retrieval_strategy
        else:
            raise HTTPException(
                status_code=400,
                detail=f"retrieval_strategy must be one of {valid_strategies}"
            )
    
    return {
        "message": "Configuration updated successfully",
        "config": system_config
    }
