
from fastapi import FastAPI
from .api.routes.query import router as query_router
from .api.routes.inguest import router as ingest_router
from .api.routes.auth import router as auth_router
from .api.routes.docker import router as docker_router
from .api.routes.eval import router as eval_router
from .api.routes.config import router as config_router
# from .api.routes.retrieval import router as retrieval_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(query_router)
app.include_router(ingest_router)
app.include_router(docker_router)
app.include_router(eval_router)
app.include_router(config_router)
# app.include_router(retrieval_router)
@app.get("/")
async def root():
    return {"message": "Hello World"}

