from fastapi import APIRouter, HTTPException, Depends
from ..Model.ingest import IngestRequest
from  .auth import get_current_user
from  services.ingestion.pipeline import DataIngestionPipeline
from rag.context_builder import set_vector_store
from services.retrieval.integration_pip_ret import vector_store_from_pipline

router = APIRouter()
DATA_DIR = "/home/marwaahmed/rag-project/RAG/data/orgin_doc"

@router.post("/ingest")
async def ingest_documents(request: IngestRequest, current_user: dict = Depends(get_current_user)):
    pipeline = DataIngestionPipeline()
    documents = pipeline.run_on_folder(request.folder_path)
    if not documents:
        raise HTTPException(status_code=404, detail="No documents found or processed in the specified folder")
    vec_store = vector_store_from_pipline(request.folder_path)
    set_vector_store(vec_store) 
    return {
        "documents": documents,
        "total_processed": len(documents)
    }


     