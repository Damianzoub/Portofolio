from pydantic import BaseModel

class Contact(BaseModel):
    name:str
    email:str 
    message:str

class Newsletter(BaseModel):
    email:str 
