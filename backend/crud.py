# backend/crud.py

from sqlalchemy.orm import Session
# --- CHANGE 1: Import 'operators' from sqlalchemy.sql ---
from sqlalchemy import or_
from sqlalchemy.sql import operators
from typing import Optional
from . import models

def comprehensive_movie_search(
    db: Session,
    title: Optional[str] = None,
    actor: Optional[str] = None,
    director: Optional[str] = None,
    genre: Optional[str] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    skip: int = 0,
    limit: int = 25,
):
    """
    Performs a comprehensive search for movies based on multiple optional criteria.
    """
    # Start with a base query for movies
    query = db.query(models.TitleBasics)

    # Filter by Title (including AKAs)
    if title:
        search_pattern = f"%{title}%"
        # JOIN with title_akas and search in primaryTitle, originalTitle, and the aka's title
        query = query.join(models.TitleAkas, isouter=True).filter(
            or_(
                models.TitleBasics.primaryTitle.ilike(search_pattern),
                models.TitleBasics.originalTitle.ilike(search_pattern),
                models.TitleAkas.title.ilike(search_pattern)
            )
        )

    # Filter by Actor or Director name
    if actor or director:
        # We need to join through principals to get to the names
        query = query.join(models.TitlePrincipals).join(models.NameBasics)
        if actor:
            actor_pattern = f"%{actor}%"
            query = query.filter(models.NameBasics.primaryName.ilike(actor_pattern))
            query = query.filter(models.TitlePrincipals.category.in_(['actor', 'actress', 'self']))
        if director:
            director_pattern = f"%{director}%"
            query = query.filter(models.NameBasics.primaryName.ilike(director_pattern))
            query = query.filter(models.TitlePrincipals.category == 'director')
            
    # Filter by Genre
    if genre:
        # --- CHANGE 2: Use the correctly imported 'ilike_op' operator ---
        query = query.filter(models.TitleBasics.genres.any(genre, operator=operators.ilike_op))

    # Filter by Year range
    if start_year:
        query = query.filter(models.TitleBasics.startYear >= start_year)
    if end_year:
        query = query.filter(models.TitleBasics.startYear <= end_year)

    # Ensure we get distinct movies, apply pagination, and execute
    return query.distinct().offset(skip).limit(limit).all()