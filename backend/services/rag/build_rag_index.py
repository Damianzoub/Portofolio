from __future__ import annotations
import re
from pathlib import Path 
from typing import List, Dict, Optional,Any,Tuple
import numpy as np 
import httpx 
import chromadb 
from chromadb.config import Settings
from .rag_types import RagDoc


def simple_chunk(text:str,chunk_size:int=900,overlap:int=140)->List[str]:
    text = re.sub(r'\s+', ' ', text).strip()
    if not text:
        return []
    out = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start+chunk_size, n)
        c = text[start:end].strip()
        if c:
            out.append(c)
        if end == n:
            break
        start = max(end - overlap, 0)
    return out 

def iter_text_files(root:Path, exts:Tuple[str,...]=(".txt",".md")):
    files = []
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in exts:
            files.append((str(p),p.read_text(encoding="utf-8",errors="ignore")))
    return files 

async def ollama_embed(texts:List[str],ollama_url:str,model:str)->List[List[float]]:
    base = ollama_url.rstrip("/")
    out:List[List[float]] = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        for t in texts:
            r = await client.post(
                f"{base}/api/embeddings",
                json={"model": model, "prompt": t},
            )
            r.raise_for_status()
            data = r.json()
            out.append(data["embedding"])
    return out 

def make_docs(content_root:str) -> List[RagDoc]:
    root = Path(content_root)
    docs: List[RagDoc] = []
    idx = 0
    for source,content in iter_text_files(root):
        chunks = simple_chunk(content)
        for c in chunks:
            docs.append(RagDoc(id=f"doc-{idx}", text=c, source=source))
            idx += 1
    return docs 

async def build_rag_index(
        content_root:str,
        persistent_dir:str,
        collection_name: str="portfolio",
        embed_provider:str="ollama",
        ollama_url = "http://localhost:11434",
        ollama_embed_model: str = "nomic-embed-text",
)-> Dict[str,Any]:
    docs = make_docs(content_root)
    if not docs:
        raise RuntimeError("No text documents found in content root")
    
    client = chromadb.PersistentClient(
        path=persistent_dir,
        settings = Settings(anonymized_telemetry=False)
    )
    col = client.get_or_create_collection(name=collection_name)
    texts = [d.text for d in docs]
    ids = [d.id for d in docs]
    metadatas = [{"source": d.source} for d in docs]

    if embed_provider != "ollama":
        raise RuntimeError(f"Unsupported embed provider: {embed_provider}")
    
    embeddings = await ollama_embed(texts,ollama_url=ollama_url,model=ollama_embed_model)

    if hasattr(col,"upsert"):
        col.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts)
    else:
        try:
            col.delete(ids=ids)
        except Exception:
            pass
        col.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts)
    
    return{
        "collection_name": collection_name,
        "persist_dir": persistent_dir,
        "count_added": len(docs),
        "embed_provider": embed_provider,
        "ollama_embed_model": ollama_embed_model,
    }
        
