from typing import Literal , Optional
from datetime import datetime 
from sqlmodel import SQLModel,Field


from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Projects(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    github_id: int = Field(index=True)
    name: str
    description: Optional[str] = None
    html_url: str
    language: Optional[str] = None
    stargazers_count: int = 0
    category: Optional[str] = "Other"
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Contacts(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str
    email:str 
    message:str
    received_at: datetime = Field(default_factory=datetime.utcnow)

class NewsletterSubscribers(SQLModel,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    email: str
    subscribed_at: datetime = Field(default_factory=datetime.utcnow)
