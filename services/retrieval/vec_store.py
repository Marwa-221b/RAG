import json
import os

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
        if len(self.chunks)==0:
            print("Warning vector store is empty. No data to search")
            return

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
    def save (self, index_path,meta_path):
        os.makedirs(os.path.dirname(index_path),exist_ok=True)
        os.makedirs(os.path.dirname(meta_path),exist_ok=True)
        faiss.write_index(self.index,index_path)
        with open (meta_path,"w",encoding="utf-8") as f:
            json.dump({
                "ids":self.ids,
                "chunks":self.chunks,
                "metadata":self.metadata
            },f)

    @classmethod
    def load(cls,index_path,meta_path,dimension):
        vs = cls(dimension)
        vs.index=faiss.read_index(index_path)
        with open(meta_path,"r",encoding="utf-8") as f:
            meta = json.load(f)
            vs.chunks=meta["chunks"]
            vs.ids=meta["ids"]
            vs.metadata=meta["metadata"]
        return vs