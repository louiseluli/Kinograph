# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# This schema is for search results - it's a lightweight view
class Movie(BaseModel):
    tconst: str
    primaryTitle: str
    originalTitle: str
    startYear: Optional[int] = None
    runtimeMinutes: Optional[int] = None
    genres: Optional[List[str]] = None

    class Config:
        from_attributes = True

# --- THIS CLASS WAS MISSING ---
# This is our schema for representing a person.
class Person(BaseModel):
    nconst: str
    primaryName: str
    birthYear: Optional[int] = None
    deathYear: Optional[int] = None
    primaryProfession: Optional[List[str]] = None
    
    class Config:
        from_attributes = True

# --- SCHEMAS FOR DETAIL VIEW ---

# Represents a single alternative title (AKA)
class Aka(BaseModel):
    title: str
    region: Optional[str] = None
    
    class Config:
        from_attributes = True

# Represents a single cast or crew member (a principal)
class Principal(BaseModel):
    nconst: str
    primaryName: str
    category: str
    # The character name is a string representation of a list, so we handle it as a string
    characters: Optional[str] = None

    class Config:
        from_attributes = True

# This is the main schema for the detailed movie view
class MovieDetail(Movie): # It inherits from our basic Movie schema
    averageRating: Optional[float] = None
    numVotes: Optional[int] = None
    
    # These fields will contain lists of other schemas
    akas: List[Aka] = []
    cast: List[Principal] = []