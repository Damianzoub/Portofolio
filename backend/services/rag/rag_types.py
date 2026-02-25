# services/rag/rag_types.py
from __future__ import annotations
from pydantic import BaseModel
from typing import Optional, Dict, Literal, List

Provider = Literal["openai", "ollama"]

class RagDoc(BaseModel):
    id: str
    text: str
    source: str
    meta: Dict[str, str] = {}

class RetrievedDoc(BaseModel):
    id: str
    text: str
    source: str
    meta: Dict[str, str]
    score: float  # Chroma returns distances; we convert to a "similarity-ish" score