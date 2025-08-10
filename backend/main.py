# backend/main.py

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kinograph API",
    description="An API for exploring movie and actor data from IMDb.",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """A welcome message for the API root."""
    return {"message": "Welcome to the Kinograph API! Go to /docs for documentation."}


# --- ADD THIS NEW ENDPOINT ---
@app.get("/people/search/", response_model=List[schemas.Person])
def search_people(name: str, db: Session = Depends(get_db)):
    """
    Search for people (actors, directors, etc.) by name.
    """
    people = crud.search_people_by_name(db=db, name=name)
    return people


# --- THIS ENDPOINT IS UPDATED ---
@app.get("/movies/search/", response_model=List[schemas.Movie])
def search_movies(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None, description="Search by movie title."),
    actor_name: Optional[str] = Query(None, description="Fuzzy search by actor name (can return multiple actors' films)."),
    director_name: Optional[str] = Query(None, description="Fuzzy search by director name."),
    actor_id: Optional[str] = Query(None, description="Precise search by actor's unique ID (nconst)."),
    director_id: Optional[str] = Query(None, description="Precise search by director's unique ID (nconst)."),
    genre: Optional[str] = Query(None, description="Filter by genre."),
    start_year: Optional[int] = Query(None, description="The earliest release year."),
    end_year: Optional[int] = Query(None, description="The latest release year.")
):
    """
    Comprehensive search for movies. Use IDs for precision.
    """
    movies = crud.comprehensive_movie_search(
        db=db, 
        title=title, 
        actor_name=actor_name, 
        director_name=director_name,
        actor_id=actor_id,
        director_id=director_id,
        genre=genre,
        start_year=start_year,
        end_year=end_year
    )
    return movies