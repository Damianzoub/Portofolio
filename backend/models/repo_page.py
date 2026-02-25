from pydantic import BaseModel
from typing import List 
from models.repo import Repo

class ProjectsPage(BaseModel):
    items: List[Repo]
    page:int
    per_page:int
    total:int
    pages:int
    has_next:bool
    has_prev:bool