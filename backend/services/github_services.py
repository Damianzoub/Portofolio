from __future__ import annotations

from typing import Optional, List, Dict, Any
import requests
import os 
from dotenv import load_dotenv
from fastapi import HTTPException

from models import Repo
load_dotenv()
GITHUB_API_BASE = os.getenv("GITHUB_API_BASE")


def _headers(token: Optional[str]) -> dict:
    h = {
        "Accept": "application/vnd.github+json",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _safe_get(url: str, headers: dict) -> Any:
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {repr(e)}")


def fetch_all_repos(username: str, token: Optional[str] = None) -> List[dict]:
    """
    Fetch ALL repos via pagination from GitHub.
    Returns raw repo dicts from GitHub.
    """
    headers = _headers(token)
    per_page = 100
    page = 1
    out: List[dict] = []

    while True:
        url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page={per_page}&page={page}&sort=pushed"
        data = _safe_get(url, headers=headers)
        if not isinstance(data, list):
            raise HTTPException(status_code=502, detail="Unexpected GitHub response format")
        if not data:
            break
        out.extend(data)
        if len(data) < per_page:
            break
        page += 1

    return out


def fetch_repo_topics(owner: str, repo_name: str, token: Optional[str] = None) -> List[str]:
    """
    GET /repos/{owner}/{repo}/topics
    """
    headers = _headers(token)
    # topics endpoint historically required this; keeping it doesn’t hurt:
    headers["Accept"] = "application/vnd.github+json"

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/topics"
    data = _safe_get(url, headers=headers)
    topics = data.get("names", [])
    if isinstance(topics, list):
        return [t for t in topics if isinstance(t, str)]
    return []


def infer_category(name: str, language: Optional[str], topics: List[str]) -> Optional[str]:
    """
    Returns one of: ML, Math, Automation, Website, or None.
    """
    n = (name or "").lower()
    lang = (language or "").lower()
    tset = set([x.lower() for x in topics])

    # 1) Topics (strongest)
    ml_topics = {"machine-learning", "deep-learning", "ml", "ai", "neural-network", "computer-vision", "nlp", "llm", "hnsw", "ann"}
    web_topics = {"react", "nextjs", "next-js", "frontend", "web", "tailwind", "typescript", "javascript"}
    auto_topics = {"automation", "bot", "scraper", "crawler", "workflow"}
    math_topics = {"math", "linear-algebra", "algebra", "geometry", "calculus"}

    if tset & ml_topics:
        return "ML"
    if tset & web_topics:
        return "Website"
    if tset & auto_topics:
        return "Automation"
    if tset & math_topics:
        return "Math"

    # 2) Language fallback
    if lang in {"typescript", "javascript", "html", "css"}:
        return "Website"
    if lang in {"python", "jupyter notebook"}:
        # python could be ML or automation; use name heuristics to split
        if any(k in n for k in ["ml", "machine", "learning", "model", "nn", "hnsw", "ann", "vector", "embedding"]):
            return "ML"
        if any(k in n for k in ["scrape", "bot", "automation", "script"]):
            return "Automation"

    # 3) Name fallback
    if any(k in n for k in ["ml", "machine-learning", "iris", "cluster", "classifier", "forecast", "nn", "embedding", "hnsw", "ann"]):
        return "ML"
    if any(k in n for k in ["math", "calculator", "calc", "algebra", "geometry", "equation", "linear-algebra"]):
        return "Math"
    if any(k in n for k in ["automation", "bot", "scraper", "script"]):
        return "Automation"
    if any(k in n for k in ["website", "portfolio", "web", "site", "html", "css", "js", "react", "next"]):
        return "Website"

    return None


def build_repo_model(item: Dict[str, Any], category: Optional[str]) -> Repo:
    return Repo(
        id=item["id"],
        name=item.get("name") or "",
        description=item.get("description"),
        html_url=item.get("html_url") or "",
        language=item.get("language"),
        stargazers_count=item.get("stargazers_count", 0),
        category=category,  # validated by Literal in Repo
    )