from datetime import datetime
from sqlmodel import Session,select
from models import Repo 
from db_models import Projects 
def sync_projects(session:Session,repos:list[Repo])->list[Repo]:
    stored: list[Projects] = []
    for repo in repos:
        db_repo = session.exec(
            select(Projects).where(Projects.github_id==repo.github_id)
        ).first()

        if db_repo:
            db_repo.name = repo.name
            db_repo.description = repo.description
            db_repo.html_url = repo.html_url 
            db_repo.language = repo.language
            db_repo.stargazers_count = repo.stargazers_count
            db_repo.category = repo.category
            db_repo.updated_at = datetime.utcnow()

        else:
            session.add(repo)
            db_repo = repo 
        stored.append(db_repo)
    session.commit()
    return stored