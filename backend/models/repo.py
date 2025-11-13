from pydantic import BaseModel
from typing import Optional,Literal

class Repo(BaseModel):
    id:int
    name:str 
    description: Optional[str]
    html_url:str
    language:Optional[str]=None
    stargazers_count: Optional[int]=0
    category: Optional[Literal["ML","Math","Automation","Website"]]=None