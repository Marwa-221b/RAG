
import os

from app.api.Model.config import system_config
from services.retrieval.integration_pip_ret import vector_store_from_pipline
from services.retrieval.retriever import retrieve


_current_vector_store = None 
def set_vector_store(vec_store):
    global _current_vector_store
    _current_vector_store = vec_store


def get_vector_store():
    global _current_vector_store
    if _current_vector_store is None:
        data_directory = system_config.get("data_directory") or os.getenv("DATA_DIRECTORY", "./data/orgin_doc")
        _current_vector_store = vector_store_from_pipline(folder_path=data_directory)
    return _current_vector_store

def get_context_from_query(query,top_k=5):
    current_vector_store = get_vector_store()
    if current_vector_store is None:
        return {"query": query, "context": "", "sources": []}
    # vec_store=vector_store_from_pipline()
    max_charss=system_config.get("max_context_chars",8000)
    results=retrieve(query,current_vector_store,top_k=top_k)
    if results:
        print("\n--- Sample Output (First Doc) ---")
        print(f"Source: {results[0]['metadata']}")
        print(f"Content (Snippet): {results[0]['chunks'][:200]}...")
    if not results:
        return {"query": query, "context": "", "sources": []}
    results=filter_chunks(results)
    results=Re_Rank(results,query)
    results=trim_chunks(results,max_chars=max_charss)
    
    context=build_context(results)
    return{
        "query":query,
        "context":context,
        "sources":results
    }


def build_context(retrieved_docs):

    context_parts = []

    for doc in retrieved_docs:

        source = doc.get("metadata", {}).get("source", "unknown")
        chunk = doc.get("chunks", "")

        formatted = f"""
[SOURCE: {source}]

{chunk}
"""

        context_parts.append(formatted)

    return "\n\n".join(context_parts)



def filter_chunks(results,min_words=5):
    filtered=[]
    for doc in results:
        chunk=doc["chunks"]
        if len(chunk.split())>=min_words:
            filtered.append(doc)

    return filtered



def Re_Rank(results,query):
    query_words=set(query.lower().split())
    scored=[]
    for doc in results:
        chunk=doc["chunks"].lower()
        overlap=sum(1 for w in query_words if w in chunk)
        scored.append((overlap,doc))
    scored.sort(reverse=True,key=lambda x:x[0])
    return  [doc for _, doc in scored]


        #     //////////////////////////// edit in enums
def trim_chunks(results,max_chars):
    selected=[]
    total=0
    for doc in results:
        chunk=doc["chunks"]
        if total+len(chunk)>max_chars:
         break
        selected.append(doc)
        total+=len(chunk)

    return selected


def format_context(results):
    context_parts = []

    for doc in results:
        text = doc["chunks"]
        source = doc["metadata"].get("source", "unknown")

        formatted = f"[Source: {source}]\n{text}"
        context_parts.append(formatted)

    return "\n\n".join(context_parts)

