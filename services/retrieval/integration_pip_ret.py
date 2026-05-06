import os.path
from sys import meta_path

from services.ingestion.pipeline import DataIngestionPipeline
from services.retrieval.chunking import chunk_text
from embeddings import embedding
from vec_store import VectorStore
from retriever import retrieve

BASE_INDEX_PATH = "../../data/vector store/indexes"
BASE_META_PATH = "../../data/vector store/meta"
BASE_PATH = "../../data"
DIMENSION=384

def vector_store_from_pipline(folder_path=None,folder_name=None):
    if folder_path:
        full_folder_path = folder_path
        save_name=folder_path.rstrip("/").split("/")[-1]
    elif folder_name:
        full_folder_path=f"{BASE_PATH}/{folder_name}"
        save_name=folder_name
    else:
        full_folder_path=BASE_PATH
        save_name="default"
    index_path = f"{BASE_INDEX_PATH}/{save_name}_index.bin"
    meta_path = f"{BASE_META_PATH}/{save_name}_meta.json"

    if os.path.exists(index_path) and os.path.exists(meta_path):
        print(f"loading existing vector store for {save_name}")
        saved_vector_store=VectorStore.load(index_path,meta_path,DIMENSION)
        return saved_vector_store

    pipline=DataIngestionPipeline()
    docs=pipline.run_on_folder(full_folder_path)
    vector_store=VectorStore(DIMENSION)

    if not docs:
        print("Warning No documents found")
        return vector_store

    for doc in docs:
        chunks=chunk_text(doc['content'])
        embedd=embedding(chunks)
        vector_store.add(embedd,chunks,doc['id'],doc['metadata'])
    vector_store.save(index_path,meta_path)
    return vector_store


if __name__ == "__main__":
    vector_store=vector_store_from_pipline(folder_name="orgin_doc")
    docs=retrieve("data prossing",vector_store)
    if docs:
        print("\n--- Sample Output (First Doc) ---")
        print(f"Source: {docs[0]['metadata']}")
        print(f"Content (Snippet): {docs[0]['chunks'][:200]}...")