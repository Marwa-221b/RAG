from sympy import true
from torch import chunk

from services.retrieval.retriever import retrieve
from services.retrieval.integration_pip_ret import vector_store_from_pipline

vec_store=vector_store_from_pipline()
def get_context_from_query(query):
    results=retrieve(query,vec_store,top_k=5)
    results=filter_chunks(results)
    results=Re_Rank(results,query)
    results=trim_chunks(results)

    context=build_context(results)
    return{
        "query":query,
        "context":context,
        "sources":results
    }


def build_context(retrieved_docs, max_chars=1500):
    context = []
    total = 0

    for doc in retrieved_docs:
        chunk = doc["chunks"]

        if total + len(chunk) > max_chars:
            break

        context.append(chunk)
        total += len(chunk)

    return "\n\n".join(context)




def filter_chunks(results,min_words=5):
    filtered=[]
    for doc in results:
        chunk=doc["chunks"]
        if len(chunk.split())>=min_words:
            filtered.append(doc)

    return filtered


# to improve ranking made in vec_store instead of only semantic similarity given by FAISS
# WE ADD 1-KEYWORD OVERLAP 2- Heuristic relevance
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
def trim_chunks(results,max_chars=1500):
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