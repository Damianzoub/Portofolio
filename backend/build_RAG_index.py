from pathlib import Path 
from typing import List 
import orjson 
from sqlmodel import Session,select
from db import engine,init_db
from db_models import Projects 
from models.rag_types import Chunk
from llm_client import embed_texts

BASE_DIR = Path(__file__).resolve().parent
BLOG_DIR = BASE_DIR.parent/ ""
INDEX_PATH = BASE_DIR/"rag_index.json"

def load_projects_chunks(session:Session)-> list[Chunk]:
    pass 

def load_blog_chunks()->list[Chunk]:
    pass 

def main():
    pass 


if __name__ =="__main__":
    main()