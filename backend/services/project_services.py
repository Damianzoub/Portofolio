from __future__ import annotations

from datetime import datetime
from typing import Iterable, List

from sqlmodel import Session, select

from db_models import Projects
from models.repo import Repo  # your pydantic Repo


def upsert_projects(session: Session, repos: Iterable[Repo]) -> List[Projects]:
    """
    Upsert GitHub repos into Projects table using github_id as unique key.
    Returns list of Projects rows (freshly updated/created).
    """
    stored: List[Projects] = []

    for repo in repos:
        db_repo = session.exec(
            select(Projects).where(Projects.github_id == repo.id)
        ).first()

        if db_repo:
            db_repo.name = repo.name
            db_repo.description = repo.description
            db_repo.html_url = repo.html_url
            db_repo.language = repo.language
            db_repo.stargazers_count = repo.stargazers_count or 0
            db_repo.category = repo.category
            db_repo.updated_at = datetime.utcnow()
        else:
            db_repo = Projects(
                github_id=repo.id,
                name=repo.name,
                description=repo.description,
                html_url=repo.html_url,
                language=repo.language,
                stargazers_count=repo.stargazers_count or 0,
                category=repo.category,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            session.add(db_repo)

        stored.append(db_repo)

    session.commit()
    return stored


def projects_to_repo(p: Projects) -> Repo:
    return Repo(
        id=p.github_id,
        name=p.name,
        description=p.description,
        html_url=p.html_url,
        language=p.language,
        stargazers_count=p.stargazers_count or 0,
        category=p.category if p.category in {"ML", "Math", "Automation", "Website"} else None,
    )