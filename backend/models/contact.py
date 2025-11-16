from pydantic import BaseModel
from datetime import datetime
class ContactIn(BaseModel):
    name:str
    email:str 
    message:str

class ContactOut(BaseModel):
    ok:bool
    message:str
    received_at:datetime





