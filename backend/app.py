import math
from datetime import datetime
from typing import List ,Optional,Literal
from fastapi import FastAPI , HTTPException,Query
from fastapi.middleware.cors import CORSMiddleware
from errors.handlers import http_403_handler,http_500_handler,http_404_handler
from models import Repo , Newsletter , ContactIn , ContactOut, ChatResponse,ChatRequest, ProjectsPage
from dotenv import load_dotenv
import os
from services.project_services import upsert_projects, projects_to_repo
from services.github_services import fetch_all_repos, fetch_repo_topics, infer_category, build_repo_model
from fastapi import Depends
from sqlmodel import Session, select,func
from db import init_db,get_session
from db_models import Projects,Contacts,NewsletterSubscribers
from utils.email_utils import send_contact_email, check_email,send_user_confirmation_email,send_subcription_confirmation_email
from pathlib import Path

load_dotenv()
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


#SMTP CONFIGS #TODO: FIX IT LATER
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT","587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
Category = Literal["All", "ML", "Math", "Automation", "Website"]
SortKey = Literal["stars", "name"]
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
    "https://damianoszoumposportofolio.vercel.app"
] #ask if i can put a list of origins in my .env

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=["*"]
)

@app.on_event("startup")
def on_startup():
    init_db()


@app.post('/assistant',response_model=ChatResponse)
async def chat_endpoint(payload:ChatRequest , session:Session = Depends(get_session))->ChatResponse:
    last_user = None 
    for msg in reversed(payload.messages):
        if msg.role == "user":
            last_user = msg.content.strip()
            break 
    
    if not last_user:
        return ChatResponse(
            reply="Tell me what you want to know about my projects, stack or CV."
        )
    text = last_user.lower()

    if "project" in text or "portfolio" in text:
        projects = session.exec(select(Projects)).all()
        if not projects:
            return ChatResponse(
                reply="I don't have any projects in database right now."
            ) 
        lines = []
        for p in projects[:5]:
            line = f"- {p.name}"
            if p.description:
                line += f": {p.description}"
            lines.append(line)
        reply=(
            "Here are some of my projects:\n" +
            "\n".join(lines)+
            "\nYou can ask me more specific questions about any of them!"
        )
        return ChatResponse(reply=reply)
    
    if "stack" in text or "tech" in text:
        return ChatResponse(
            reply="My stack is Python (FastAPI,ML,data), Next.js + Tailwind for frontend and SQLModel + SQLite for storage."
        )
    if "cv" in text or "resume" in text:
        return ChatResponse(
            reply="You can find my CV at https://damianos.dev/cv"
        )
    return ChatResponse(
        reply="Tell me what you want to know about my projects, stack or CV."
    )
@app.get('/health')
async def health():
    return {"status":"ok"}

@app.post("/projects/sync")
def sync_projects_from_github(session: Session = Depends(get_session)):
    raw = fetch_all_repos(GITHUB_USER, GITHUB_TOKEN)

    repos: list[Repo] = []
    for item in raw:
        name = item.get("name") or ""
        if name == GITHUB_USER:
            continue

        topics = fetch_repo_topics(GITHUB_USER, name, GITHUB_TOKEN)
        category = infer_category(name=name, language=item.get("language"), topics=topics)
        repos.append(build_repo_model(item, category))

    stored = upsert_projects(session, repos)
    return {"synced": len(stored)}

@app.get("/projects", response_model=ProjectsPage)
def list_projects(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(12, ge=1, le=50),
    category: Category = Query("All"),
    search: Optional[str] = Query(None),
    sort: SortKey = Query("stars"),
):
    q = select(Projects)

    if category != "All":
        q = q.where(Projects.category == category)

    if search:
        s = f"%{search.lower()}%"
        q = q.where(func.lower(Projects.name).like(s) | func.lower(func.coalesce(Projects.description, "")).like(s))

    # sorting
    if sort == "stars":
        q = q.order_by(Projects.stargazers_count.desc(), Projects.name.asc())
    else:
        q = q.order_by(Projects.name.asc())

    # total count
    count_q = select(func.count()).select_from(q.subquery())
    total = session.exec(count_q).one()
    pages = max(1, math.ceil(total / per_page))

    # pagination
    offset = (page - 1) * per_page
    items_db = session.exec(q.offset(offset).limit(per_page)).all()
    items = [projects_to_repo(p) for p in items_db]

    return ProjectsPage(
        items=items,
        page=page,
        per_page=per_page,
        total=total,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )

@app.post('/contact',response_model=ContactOut)
async def submit_contact(contact:ContactIn, session: Session = Depends(get_session)):
    
    if not check_email(contact.email):
        return {"ok":False,"message":"Invalid email address."}
    if len(contact.message.strip())==0:
        return {"ok":False,"message":"Message cannot be empty."}
    if len(contact.name.strip())==0:
        return {"ok":False,"message":"Name cannot be empty."}
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
    print('ok')
    if check_email(body.email):
        print("ok")
        existing = session.exec(
            select(NewsletterSubscribers).where(NewsletterSubscribers.email==body.email)
        ).first()
        if existing:
            raise HTTPException(status_code=400,detail="Email already subscribed.")
        sub = NewsletterSubscribers(
            email = body.email
        )
        session.add(sub)
        session.commit()
        session.refresh(sub)
        try:
            send_subcription_confirmation_email(
                smtp_host=SMTP_HOST,
                smtp_port=SMTP_PORT,
                smtp_user = SMTP_USER,
                smtp_pass = SMTP_PASSWORD,
                sender = SMTP_USER,
                user_email = body.email,
                user_name = body.email.split("@")[0]
            )
        except Exception as e:
            return {"ok":False,"message":"Failed to send confirmation email."}
        return {"ok":True,"message":"Subscribed to newsletter!"}
    else:
        return {"ok":False,"message":"Invalid email address."}
