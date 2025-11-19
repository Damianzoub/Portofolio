from datetime import datetime
from typing import List 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from errors.handlers import http_403_handler,http_500_handler,http_404_handler
from models import Repo , Newsletter , ContactIn , ContactOut
from dotenv import load_dotenv 
import os
from services.project_services import sync_projects
from fastapi import Depends
from sqlmodel import Session, select
from db import init_db,get_session
from db_models import Projects,Contacts,NewsletterSubscribers
from utils.email_utils import send_contact_email, check_email,send_user_confirmation_email
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
FORBIDDEN_EMAIL = os.getenv("FORBIDDEN_EMAIL")
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

@app.on_event("startup")
def on_startup():
    init_db()

@app.get('/health')
async def health():
    return {"status":"ok"}

@app.get("/projects", response_model=List[Repo])
async def list_projects(session: Session = Depends(get_session)):
    gh_repos = fetch_repos_for_user(GITHUB_USER)  # whatever args

    # 1) GitHub -> Projects (DB models)
    project_models: list[Projects] = []
    for r in gh_repos:
        project_models.append(
            Projects(
                github_id=r.id,                             # GitHub ID
                name=r.name,
                description=getattr(r, "description", None),
                html_url=r.html_url,                        # ✅ required later for Repo
                language=getattr(r, "language", None),
                stargazers_count=getattr(r, "stargazers_count", 0),
                # category you can fill later from config / mapping
            )
        )

    stored_projects = sync_projects(session, project_models)

    # 2) Projects (DB) -> Repo (response schema)
    repos_response: list[Repo] = []
    for p in stored_projects:
        repos_response.append(
            Repo(
                id=p.github_id,                 # frontend sees GitHub ID as id
                name=p.name,
                description=p.description,
                html_url=p.html_url,
                language=p.language,
                stargazers_count=p.stargazers_count,
                category=p.category if p.category in {"ML", "Math", "Automation", "Website"} else None,
            )
        )

    return repos_response

@app.post('/contact',response_model=ContactOut)
async def submit_contact(contact:ContactIn, session: Session = Depends(get_session)):
    # later: store in db or send email
    if not check_email(contact.email):
        return {"ok":False,"message":"Invalid email address."}
    if len(contact.message.strip())==0:
        return {"ok":False,"message":"Message cannot be empty."}
    if len(contact.name.strip())==0:
        return {"ok":False,"message":"Name cannot be empty."}
    if contact.email == FORBIDDEN_EMAIL:
        return {"ok":False,"message":"Forbidden email address."}
    try:
        send_contact_email(
            smtp_host=SMTP_HOST,
            smtp_port=SMTP_PORT,
            smtp_user = SMTP_USER,
            smtp_pass = SMTP_PASSWORD,
            sender = SMTP_USER,
            recipient = SMTP_USER,
            name = contact.name,
            email = contact.email,
            message = contact.message
        )
    except Exception as e:
        return {"ok":False,"message":"Failed to send message."}
    try:
        send_user_confirmation_email(
            smtp_host=SMTP_HOST,
            smtp_port=SMTP_PORT,
            smtp_user = SMTP_USER,
            smtp_pass = SMTP_PASSWORD,
            sender = SMTP_USER,
            user_email = contact.email,
            user_name = contact.name
        )
    except Exception as e:
        return {"ok":False,"message":"Failed to log message."}
    msg = Contacts(
        name = contact.name,
        email = contact.email,
        message = contact.message
    )
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return ContactOut(
        ok=True,
        message="Thanks for reaching out! I'll get back to you soon.",
        received_at=msg.received_at
    )

@app.post('/newsletter')
async def subscribe_newsletter(body:Newsletter,session: Session = Depends(get_session)):
    # later: store in db or send email
    if check_email(body.email):
        sub = NewsletterSubscribers(
            email = body.email
        )
        session.add(sub)
        session.commit()
        session.refresh(sub)
        return {"ok":True,"message":"Subscribed to newsletter!"}
    else:
        return {"ok":False,"message":"Invalid email address."}