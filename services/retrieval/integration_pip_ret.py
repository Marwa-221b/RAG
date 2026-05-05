from services.ingestion.pipeline import DataIngestionPipeline
from services.retrieval.chunking import chunk_text
from embeddings import embedding
from vec_store import VectorStore
from retriever import retrieve

def vector_store_from_pipline(folder_path="../../data",dimension=384):
    pipline=DataIngestionPipeline()
    docs=pipline.run_on_folder(folder_path)
    vector_store=VectorStore(dimension)
    for doc in docs:
        chunks=chunk_text(doc['content'])
        embedd=embedding(chunks)
        vector_store.add(embedd,chunks,doc['id'],doc['metadata'])

    return vector_store


if __name__ == "__main__":
    vector_store=vector_store_from_pipline()
    docs=retrieve("data prossing",vector_store)
    if docs:
        print("\n--- Sample Output (First Doc) ---")
        print(f"Source: {docs[0]['metadata']}")
        print(f"Content (Snippet): {docs[0]['chunks'][:200]}...")