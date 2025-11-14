from typing import List 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from errors.handlers import http_403_handler,http_500_handler,http_404_handler
from models import Repo , ContactIn, Newsletter
from utils.email_check import check_email


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

SAMPLE_PROJECTS: List[Repo] = [
    Repo(
        id=1,
        name="Iris Classifier",
        description="End-to-end ML pipeline with FastAPI inference.",
        html_url="https://github.com/Damianzoub/ml-project-iris",
        language="Python",
        stargazers_count=0,
        category="ML",
    ),
    Repo(
        id=2,
        name="Mall Customers Clustering",
        description="KMeans + EDA for customer segmentation.",
        html_url="https://github.com/Damianzoub/Mall_Customers_Clustering",
        language="Python",
        stargazers_count=0,
        category="ML",
    ),
    Repo(
        id=3,
        name="Time Series Forecast",
        description="Classical time series forecasting with evaluation.",
        html_url="https://github.com/Damianzoub/time-series-project",
        language="Python",
        stargazers_count=0,
        category="ML",
    ),
    Repo(
        id=4,
        name="NewsScrapingAPI",
        description="Scrapes news + sentiment classification via TextBlob.",
        html_url="https://github.com/Damianzoub/news-scraping-api",
        language="Python",
        stargazers_count=0,
        category="Automation",
    ),
    Repo(
        id=5,
        name="Math Utils",
        description="Small numeric helpers and math utilities.",
        html_url="https://github.com/Damianzoub/math-utils",
        language="JavaScript",
        stargazers_count=0,
        category="Math",
    ),
    Repo(
        id=6,
        name="Portfolio Website",
        description="Next.js + Tailwind personal portfolio.",
        html_url="https://github.com/Damianzoub/portfolio",
        language="TypeScript",
        stargazers_count=0,
        category="Website",
    ),
]

@app.get('/health')
async def health():
    return {"status":"ok"}

@app.get('/projects',response_model=list[Repo])
async def list_projects()-> list[Repo]:
    return SAMPLE_PROJECTS

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