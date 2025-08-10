# backend/crud.py

from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.sql import operators
from typing import Optional
from . import models

# --- ADD THIS NEW FUNCTION ---
def search_people_by_name(db: Session, name: str, limit: int = 25):
    """Searches for people by their primary name."""
    search_pattern = f"%{name}%"
    return db.query(models.NameBasics).filter(models.NameBasics.primaryName.ilike(search_pattern)).limit(limit).all()


def comprehensive_movie_search(
    db: Session,
    title: Optional[str] = None,
    actor_name: Optional[str] = None,
    director_name: Optional[str] = None,
    # --- ADD NEW PARAMETERS ---
    actor_id: Optional[str] = None,
    director_id: Optional[str] = None,
    genre: Optional[str] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    skip: int = 0,
    limit: int = 25,
):
    """
    Performs a comprehensive search for movies based on multiple optional criteria.
    """
    query = db.query(models.TitleBasics)

    if title:
        search_pattern = f"%{title}%"
        query = query.join(models.TitleAkas, isouter=True).filter(
            or_(
                models.TitleBasics.primaryTitle.ilike(search_pattern),
                models.TitleBasics.originalTitle.ilike(search_pattern),
                models.TitleAkas.title.ilike(search_pattern)
            )
        )

    # --- THIS LOGIC IS NOW UPDATED ---
    # Prioritize searching by specific ID if provided
    if actor_id or director_id:
        query = query.join(models.TitlePrincipals)
        if actor_id:
            query = query.filter(models.TitlePrincipals.nconst == actor_id)
        if director_id:
            query = query.filter(models.TitlePrincipals.nconst == director_id)
    # Fallback to searching by name if no ID is given
    elif actor_name or director_name:
        query = query.join(models.TitlePrincipals).join(models.NameBasics)
        if actor_name:
            query = query.filter(models.NameBasics.primaryName.ilike(f"%{actor_name}%"))
            query = query.filter(models.TitlePrincipals.category.in_(['actor', 'actress', 'self']))
        if director_name:
            query = query.filter(models.NameBasics.primaryName.ilike(f"%{director_name}%"))
            query = query.filter(models.TitlePrincipals.category == 'director')
            
    if genre:
        query = query.filter(models.TitleBasics.genres.any(genre, operator=operators.ilike_op))

    if start_year:
        query = query.filter(models.TitleBasics.startYear >= start_year)
    if end_year:
        query = query.filter(models.TitleBasics.startYear <= end_year)

    return query.distinct().offset(skip).limit(limit).all()