# backend/main.py

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

# Import our new modules
from . import crud, models, schemas
from .database import get_db, engine

# Create the database tables if they don't exist
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

# This is our new and improved search endpoint
@app.get("/movies/search/", response_model=List[schemas.Movie])
def search_movies(
    db: Session = Depends(get_db), # <-- This line is now corrected
    title: Optional[str] = Query(None, description="Search by movie title (including alternative titles)."),
    actor: Optional[str] = Query(None, description="Search for movies by actor name."),
    director: Optional[str] = Query(None, description="Search for movies by director name."),
    genre: Optional[str] = Query(None, description="Filter movies by a specific genre."),
    start_year: Optional[int] = Query(None, description="The earliest release year."),
    end_year: Optional[int] = Query(None, description="The latest release year.")
):
    """
    Comprehensive search for movies based on various criteria.
    All parameters are optional. Combine them to refine your search.
    """
    movies = crud.comprehensive_movie_search(
        db=db, 
        title=title, 
        actor=actor, 
        director=director,
        genre=genre,
        start_year=start_year,
        end_year=end_year
    )
    return movies