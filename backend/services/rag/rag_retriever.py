from __future__ import annotations
from typing import List 
import httpx 
import chromadb
from chromadb.config import Settings
from rag.rag_types import RagDoc, RetrievedDoc

async def ollama_embed_one(text:str,ollama_url:str,model:str)->List[float]:
    base = ollama_url.rstrip("/")
    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            f"{base}/api/embeddings",
            json={"model": model, "prompt": text},
        )
        r.raise_for_status()
        data = r.json()
        return data["embedding"]

class RagRetriever:
    def  __init__(self,persist_dir:str="rag_store_chroma",collection_name:str="portofolio",ollama_url:str="http://localhost:11434",ollama_embed_model:str="nomic-embed-text"):
        self.ollama_url = ollama_url
        self.ollama_embed_model = ollama_embed_model
        self.client = chromadb.PersistentClient(Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir))
        self.collection = self.client.get_or_create_collection(name=collection_name)
    
    async def retrieve(self, query:str, top_k:int=5) -> List[RetrievedDoc]:
        q_embed = await ollama_embed_one(query,self.ollama_url,self.ollama_embed_model)
        res = self.collection.query(
            query_embeddings=[q_embed],
            n_results=top_k,
            include=["metadatas", "documents"]
        )
        #chroma returns lists per query
        ids = res["ids"][0]
        docs= res["documents"][0]
        metas = res["metadatas"][0]
        dists = res["distances"][0]

        out: List[RetrievedDoc] = []
        for _id, doc, meta, dist in zip(ids, docs, metas, dists):
            score = 1.0/(1.0+float(dist))
            out.append(
                RetrievedDoc(id=_id, text=doc, source=meta.get("source",""), meta=meta, score=score)
            )
        return out