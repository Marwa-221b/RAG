from fastapi import FastAPI
from .api.routes.query import router as query_router
from .api.routes.inguest import router as ingest_router
from .api.routes.auth import router as auth_router

app = FastAPI()

# app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(query_router)
app.include_router(ingest_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
