#placeholder code##
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Local RAG API",
    description="Retrieval-Augmented Generation system",
    version="1.0.0"
)

# Allow frontend / Postman to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "RAG API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}