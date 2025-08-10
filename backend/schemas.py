# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# This schema is for our movie search results.
class Movie(BaseModel):
    tconst: str
    primaryTitle: str
    originalTitle: str
    startYear: Optional[int] = None
    runtimeMinutes: Optional[int] = None
    genres: Optional[List[str]] = None

    class Config:
        from_attributes = True

# --- ADD THIS NEW CLASS ---
# This is our new schema for representing a person.
class Person(BaseModel):
    nconst: str
    primaryName: str
    birthYear: Optional[int] = None
    deathYear: Optional[int] = None
    primaryProfession: Optional[List[str]] = None
    
    class Config:
        from_attributes = True