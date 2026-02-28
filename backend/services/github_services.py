from __future__ import annotations

from typing import Optional, List, Dict, Any, Iterable, Tuple
import os
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from fastapi import HTTPException


from models import Repo

GITHUB_API_BASE = os.getenv("GITHUB_API_BASE", "https://api.github.com")


# ---------- HTTP client (session + retries) ----------

def _make_session() -> requests.Session:
    s = requests.Session()

    # Retry only on transient failures / rate limiting.
    retry = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        raise_on_status=False,
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def _headers(token: Optional[str], accept: str = "application/vnd.github+json") -> dict:
    h = {"Accept": accept}
    if token:
        # GitHub accepts Bearer tokens (fine) or token <...> for classic tokens.
        h["Authorization"] = f"Bearer {token}"
    return h


def _safe_get(s: requests.Session, url: str, headers: dict, timeout: float = 10.0) -> Any:
    try:
        resp = s.get(url, headers=headers, timeout=timeout)
        # If retry exhausted, you may still get e.g. 502. Surface clean error.
        if resp.status_code >= 400:
            # helpful GitHub error payload when present
            try:
                payload = resp.json()
            except Exception:
                payload = {"message": resp.text[:200]}
            raise HTTPException(
                status_code=502,
                detail=f"GitHub API error {resp.status_code}: {payload.get('message', 'unknown')}",
            )
        return resp.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"GitHub API error: {repr(e)}")


# ---------- API functions ----------

def fetch_all_repos(username: str, token: Optional[str] = None) -> List[dict]:
    """
    Fetch ALL repos via pagination from GitHub.
    Sorted by pushed time so the most recent appear first.
    """
    s = _make_session()
    headers = _headers(token)

    per_page = 100
    page = 1
    out: List[dict] = []

    while True:
        url = f"{GITHUB_API_BASE}/users/{username}/repos?per_page={per_page}&page={page}&sort=pushed"
        data = _safe_get(s, url, headers=headers, timeout=10.0)

        if not isinstance(data, list):
            raise HTTPException(status_code=502, detail="Unexpected GitHub response format (expected list)")

        if not data:
            break

        out.extend(data)

        if len(data) < per_page:
            break

        page += 1

    return out


def fetch_repo_topics(owner: str, repo_name: str, token: Optional[str] = None, *, session: Optional[requests.Session] = None) -> List[str]:
    """
    GET /repos/{owner}/{repo}/topics
    Note: topics sometimes require a preview Accept header on older stacks.
    """
    s = session or _make_session()

    # This Accept header historically was required; still safe.
    headers = _headers(token, accept="application/vnd.github.mercy-preview+json")

    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/topics"
    data = _safe_get(s, url, headers=headers, timeout=10.0)

    topics = data.get("names", [])
    if isinstance(topics, list):
        return [t for t in topics if isinstance(t, str)]
    return []


def fetch_repo_topics_many(
    owner: str,
    repo_names: Iterable[str],
    token: Optional[str] = None,
    *,
    max_workers: int = 6,
) -> Dict[str, List[str]]:
    """
    Fetch topics for many repos concurrently.
    Returns dict repo_name -> topics.
    Use with care (rate limits).
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    names = list(repo_names)
    if not names:
        return {}

    s = _make_session()
    out: Dict[str, List[str]] = {}

    # small pool to avoid triggering abuse rate limits
    workers = max(1, min(max_workers, 10))

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {
            ex.submit(fetch_repo_topics, owner, name, token, session=s): name
            for name in names
        }
        for fut in as_completed(futs):
            name = futs[fut]
            try:
                out[name] = fut.result()
            except Exception:
                out[name] = []

    return out


# ---------- Categorization ----------

def infer_category(name: str, language: Optional[str], topics: List[str]) -> Optional[str]:
    """
    Returns one of: ML, Math, Automation, Website, or None.
    """
    n = (name or "").lower()
    lang = (language or "").lower()
    tset = {x.lower() for x in topics if isinstance(x, str)}

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

    if lang in {"typescript", "javascript", "html", "css"}:
        return "Website"

    if lang in {"python", "jupyter notebook"}:
        if any(k in n for k in ("ml", "machine", "learning", "model", "nn", "hnsw", "ann", "vector", "embedding")):
            return "ML"
        if any(k in n for k in ("scrape", "bot", "automation", "script")):
            return "Automation"

    if any(k in n for k in ("ml", "machine-learning", "iris", "cluster", "classifier", "forecast", "nn", "embedding", "hnsw", "ann")):
        return "ML"
    if any(k in n for k in ("math", "calculator", "calc", "algebra", "geometry", "equation", "linear-algebra")):
        return "Math"
    if any(k in n for k in ("automation", "bot", "scraper", "script")):
        return "Automation"
    if any(k in n for k in ("website", "portfolio", "web", "site", "html", "css", "js", "react", "next")):
        return "Website"

    return None


def build_repo_model(item: Dict[str, Any], category: Optional[str]) -> Repo:
    return Repo(
        id=item["id"],
        name=item.get("name") or "",
        description=item.get("description"),
        html_url=item.get("html_url") or "",
        language=item.get("language"),
        stargazers_count=int(item.get("stargazers_count", 0) or 0),
        category=category,
    )