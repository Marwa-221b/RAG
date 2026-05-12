from services.retrieval.embeddings import model
from services.retrieval.vec_store import VectorStore

def retrieve(query,vec_store,top_k=5):
    query_embedding=model.encode([query])
    results=vec_store.search(query_embedding,top_k)
    for result in results:
        if 'metadata' in result and 'source' not in result['metadata']:
            # Add source if missing
            result['metadata']['source'] = result.get('source', 'unknown')
        elif 'metadata' not in result:
            result['metadata'] = {'source': result.get('source', 'unknown')}
    
    return results