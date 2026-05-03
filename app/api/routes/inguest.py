from fastapi import APIRouter, HTTPException, Depends
from ..Model.ingest import IngestRequest
from  .auth import get_current_user
from ....services.ingestion.pipline import DataIngestionPipeline

router = APIRouter()

@router.post("/ingest")
async def ingest_documents(request: IngestRequest, current_user: dict = Depends(get_current_user)):
    pipeline = DataIngestionPipeline()
    documents = pipeline.run_on_folder(request.folder_path)
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found or processed in the specified folder")
    return {
        "documents": documents,
        "total_processed": len(documents)
    }