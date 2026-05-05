from services.retrieval.embeddings import model
from services.retrieval.vec_store import VectorStore

def retrieve(query,vec_store,top_k=2):
    query_embedding=model.encode([query])
    results=vec_store.search(query_embedding,top_k)
    return results