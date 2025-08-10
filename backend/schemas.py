# backend/schemas.py

from pydantic import BaseModel
from typing import List, Optional

# This is our Pydantic model, or "schema".
# It defines the data shape for a movie when reading it from the API.
class Movie(BaseModel):
    tconst: str
    primaryTitle: str
    originalTitle: str
    startYear: Optional[int] = None
    runtimeMinutes: Optional[int] = None
    genres: Optional[List[str]] = None

    # This config class tells Pydantic to read data even if it's not a dict,
    # but an ORM model (our database model).
    # 'from_attributes=True' is the updated version of 'orm_mode=True'.
    class Config:
        from_attributes = True