from typing import List, Optional
import os 
import requests
from models import Repo 
GITHUB_API_BASE = "https://api.github.com"

def fetch_repos_for_user(username:str,token: Optional[str]=None)-> list[Repo]:
    url = f"{GITHUB_API_BASE}/users/{username}/repos"
    headers = {"Accept":"application/vnd.github+json"}
    if token:
        headers['Authorization'] = f"Bearer {token}"
    
    resp = requests.get(url,headers=headers,timeout=10)
    data = resp.json()

    repos: list[Repo]= []
    for item in data:
        category = None
        if item['name']:
            lowered_name = item['name'].lower()
            if any( k in lowered_name for k in ['ml','machine-learning','iris','cluster','classifier','forecast','nn','ml']):
                category="ML"
            elif any( k in lowered_name for k in ['math','calculator','calc','algebra','geometry','equation','linear-algebra']):
                category = "Math"
            elif any( k in lowered_name for k in ['automation','bot','scraper','script']):
                category = "Automation"
            elif any( k in lowered_name for k in ['website','portfolio','web','site','html','css','js','react']):
                category = "Website"

        if item['name'] == "Damianzoub":
            continue
        
        repo = Repo(
            id = item['id'],
            name = item['name'],
            description = item['description'],
            html_url = item['html_url'],
            language = item['language'],
            stargazers_count = item['stargazers_count'],
            category = category
        )
        repos.append(repo)
    return repos