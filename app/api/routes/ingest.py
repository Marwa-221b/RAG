from fastapi import APIRouter, HTTPException, Depends
from ..Model.ingest import IngestRequest
from .auth import get_current_user
from services.ingestion.pipeline import DataIngestionPipeline
import os

router = APIRouter()

@router.post("/ingest")
async def ingest_documents(request: IngestRequest, current_user: dict = Depends(get_current_user)):
    pipeline = DataIngestionPipeline()
    
    # Use folder_path from request, fallback to env variable
    folder = request.folder_path or os.getenv("DATA_PATH", "/app/data")
    
    documents = pipeline.run_on_folder(folder)
    if not documents:
        raise HTTPException(
            status_code=404, 
            detail=f"No documents found in: {folder}"
        )
    return {
        "documents": documents,
        "total_processed": len(documents)
    }