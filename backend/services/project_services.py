# services/project_services.py
from __future__ import annotations

from datetime import datetime
from typing import Iterable, List, Dict

from sqlmodel import Session, select

from db_models import Projects
from models.repo import Repo


def upsert_projects_fast(session: Session, repos: Iterable[Repo]) -> List[Projects]:
    repos = list(repos)
    if not repos:
        return []

    ids = [r.id for r in repos]

    # ONE query to fetch existing rows
    existing_rows = session.exec(
        select(Projects).where(Projects.github_id.in_(ids))
    ).all()
    existing: Dict[int, Projects] = {p.github_id: p for p in existing_rows}

    now = datetime.utcnow()
    stored: List[Projects] = []

    for repo in repos:
        db_repo = existing.get(repo.id)

        if db_repo:
            # update only what you need
            db_repo.name = repo.name
            db_repo.description = repo.description
            db_repo.html_url = repo.html_url
            db_repo.language = repo.language
            db_repo.stargazers_count = int(repo.stargazers_count or 0)
            db_repo.category = repo.category
            db_repo.updated_at = now
        else:
            db_repo = Projects(
                github_id=repo.id,
                name=repo.name,
                description=repo.description,
                html_url=repo.html_url,
                language=repo.language,
                stargazers_count=int(repo.stargazers_count or 0),
                category=repo.category,
                created_at=now,
                updated_at=now,
            )
            session.add(db_repo)

        stored.append(db_repo)

    session.commit()
    return stored