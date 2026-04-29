import faiss
import numpy as np

class VectorStore:
    def __init__(self,dimension):
        self.index=faiss.IndexFlatIP(dimension)
        self.chunks=[]

    def normalize(self,embedding):
        norm=np.linalg.norm(embedding,axis=1,Keepdims=True)
        return embedding/norm

    def add(self,embedding , chunks):
        norm=self.normalize(np.array(embedding))
        self.index.add(norm)
        self.chunks.extend(chunks)

    def search(self,query,top_k=2):
        norm_query=self.normalize(np.array(query))
        dist,indices=self.index.search(norm_query,top_k)
        chunks=[self.chunks[i] for i in indices[0]]
        return chunks
