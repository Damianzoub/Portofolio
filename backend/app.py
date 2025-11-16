from typing import List 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from errors.handlers import http_403_handler,http_500_handler,http_404_handler
from models import Repo , Newsletter , ContactIn , ContactOut
from backend.utils.email_utils import check_email
from dotenv import load_dotenv 
import os
from client.github_client import fetch_repos_for_user
from pathlib import Path
load_dotenv()
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

#SMTP CONFIGS #TODO: FIX IT LATER
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT","587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
CONTACT_LOG = Path("contact_messages.jsonl")
app = FastAPI(
    title="Damian Portofolio API",
    description="Backend API For Damianos Portofolio "
)

app.add_exception_handler(404,http_404_handler)
app.add_exception_handler(500,http_500_handler)
app.add_exception_handler(403,http_403_handler)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"]
)



@app.get('/health')
async def health():
    return {"status":"ok"}

@app.get('/projects',response_model=list[Repo])
async def list_projects()-> list[Repo]:
    repos = fetch_repos_for_user(GITHUB_USER,GITHUB_TOKEN)
    return repos

@app.post('/contact')
async def submit_contact(contact:ContactIn):
    # later: store in db or send email
    if not check_email(contact.email):
        return {"ok":False,"message":"Invalid email address."}
    if len(contact.message.strip())==0:
        return {"ok":False,"message":"Message cannot be empty."}
    if len(contact.name.strip())==0:
        return {"ok":False,"message":"Name cannot be empty."}
    return {"ok":True,"message":"Thanks for reaching out!"}

@app.post('/newsletter')
async def subscribe_newsletter(body:Newsletter):
    # later: store in db or send email
    if check_email(body.email):
        return {"ok":True,"message":"Subscribed to newsletter!"}
    else:
        return {"ok":False,"message":"Invalid email address."}