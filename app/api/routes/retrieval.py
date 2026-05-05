# from services.retrieval.retriever import Retriever
# from fastapi import APIRouter, Depends

# router = APIRouter()

# @router.post("/retrieve")
# async def call_retrieval_service(query: str, top_k: int):
#     retriever = Retriever()
#     results = retriever.search(query, top_k)
#     return results