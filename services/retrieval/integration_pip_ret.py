import os.path
from sys import meta_path

import os
from services.ingestion.pipeline import DataIngestionPipeline
from services.retrieval.chunking import chunk_text
from services.retrieval.embeddings import embedding
from services.retrieval.vec_store import VectorStore
from services.retrieval.retriever import retrieve
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR, "..", "..")

BASE_PATH = os.getenv("DATA_PATH", "/app/data")
BASE_INDEX_PATH = os.getenv("DATA_INDEX_PATH", "/app/data/vector_store/indexes")
BASE_META_PATH = os.getenv("DATA_META_PATH", "/app/data/vector_store/meta")
DIMENSION = 384

# BASE_INDEX_PATH = os.path.join(PROJECT_ROOT, "data", "vector_store", "indexes")
# BASE_META_PATH  = os.path.join(PROJECT_ROOT, "data", "vector_store", "meta")
# BASE_PATH = "../../data"
# DIMENSION=384
# >>>>>>> origin/main

def vector_store_from_pipline(folder_path=None, folder_name=None):
    if folder_path:
        full_folder_path = folder_path
        save_name = os.path.basename(folder_path.rstrip("/\\"))
    elif folder_name:
        full_folder_path = os.path.join(PROJECT_ROOT, "data", folder_name)
        save_name = folder_name
    else:
        full_folder_path = os.path.join(PROJECT_ROOT, "data")
        save_name = "default"

    index_path = os.path.join(BASE_INDEX_PATH, f"{save_name}_index.bin")
    meta_path  = os.path.join(BASE_META_PATH,  f"{save_name}_meta.json")

    if os.path.exists(index_path) and os.path.exists(meta_path):
        print(f"Loading existing vector store for {save_name}")
        return VectorStore.load(index_path, meta_path, DIMENSION)


    pipeline = DataIngestionPipeline()
    docs = pipeline.run_on_folder(full_folder_path)
    vector_store = VectorStore(DIMENSION)


    if not docs:
        print("Warning: No documents found")
        return vector_store

    for doc in docs:
        chunks = chunk_text(doc['content'])
        embedd = embedding(chunks)
        vector_store.add(embedd, chunks, doc['id'], doc['metadata'])

    vector_store.save(index_path, meta_path)
    return vector_store

if __name__ == "__main__":
    vector_store=vector_store_from_pipline(folder_name="orgin_doc")
    docs=retrieve("data prossing",vector_store)
    if docs:
        print("\n--- Sample Output (First Doc) ---")
        print(f"Source: {docs[0]['metadata']}")
        print(f"Content (Snippet): {docs[0]['chunks'][:200]}...")