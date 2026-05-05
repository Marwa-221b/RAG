import faiss
import numpy as np

class VectorStore:
    def __init__(self,dimension):
        self.index=faiss.IndexFlatIP(dimension)
        self.chunks=[]
        self.ids=[]
        self.metadata=[]

    @staticmethod
    def normalize(embedding):
        norm=np.linalg.norm(embedding,axis=1,keepdims=True)
        return embedding/norm

    def add(self,embedding , chunks,doc_id,metadata=None):
        norm=self.normalize(np.array(embedding))
        self.index.add(norm)
        self.chunks.extend(chunks)
        self.ids.extend([doc_id]*len(chunks))
        if metadata:
            self.metadata.extend([metadata]*len(chunks))

    def search(self,query,top_k=2):
        norm_query=self.normalize(np.array(query))
        dist,indices=self.index.search(norm_query,top_k)
        results=[]
        for i in indices[0]:
            results.append({
                "chunks":self.chunks[i],
                "doc_id":self.ids[i],
                "metadata":self.metadata[i]
            })
        return results
