from dataclasses import dataclass
from typing import List 

@dataclass
class Chunk:
    id: str 
    source: str
    title: str
    text: str 
    embedding: List[float]