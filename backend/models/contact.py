from pydantic import BaseModel

class ContactIn(BaseModel):
    name:str
    email:str 
    message:str




